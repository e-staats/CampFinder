import * as React from 'react';
import Button from './resources/Button';
import MapBody from './resources/MapBody';

export interface Props {
  handleChange(arg1: React.ChangeEvent<HTMLInputElement>, arg2: string): any,
  parks: InputData,
}

export interface RegionInput {
  allChecked: boolean,
  link: string,
  name: string,
  parkList: Park[]
}

export interface InputData {
  allChecked: boolean,
  northeast: RegionInput,
  northwest: RegionInput,
  southeast: RegionInput,
  southwest: RegionInput,
}

export interface Park {
  id: number,
  name: string,
  isChecked: boolean,
  lat: number,
  lng: number,
  time?: string,
  distance?: string,
}

export interface NodeInfo {
  id: string,
  name: string,
  color: string,
  xPos: number,
  yPos: number,
  region?: string,
  isChecked?: boolean,
  onClick?(): any,
}

export interface Boundaries {
  north: number,
  south: number,
  east: number,
  west: number,
}

export interface PixelRates {
  lat: number,
  long: number,
}

export interface ServerLocationData {
  parks: Park
}

export interface ServerDistanceData {
  origin: Park,
  parks: Distance,
}

export interface Distance {
  [id: string]: {
    time: string,
    distance: string,
  }
}

interface State {
  nodes: NodeInfo[],
  zipCode: string,
  origin: NodeInfo,
}

class Map extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      nodes: [],
      zipCode: "",
      origin: {
        id: '0',
        name: 'undefined',
        xPos: 0,
        yPos: 0,
        color: 'FFFFFF',
      },
    }
  }

  componentDidMount() {
    this.setState(() => {
      let nodes = this.createNodesForParks(this.props.parks)
      return { nodes }
    })
  }

  componentDidUpdate(prevProps) {
    console.log("I see that the props have changed...")
    console.log(JSON.stringify(prevProps.parks))
    console.log(JSON.stringify(this.props.parks))
    if (this.props.parks !== prevProps.parks) {
      this.updateCheckedStatus(this.props.parks, prevProps.parks)
    }
  }

  updateCheckedStatus = (parks: InputData, prevParks: InputData) => {
    let parksToUpdate: { [id: number]: boolean } = {}
    for (let region in parks) {
      if (region === 'allChecked') { continue }
      for (let park of parks[region]) {
        for (let prevPark of prevParks[region]) {
          if (park.isChecked !== prevPark.isChecked) {
            parksToUpdate[park.id] = park.isChecked
          }
        }
      }
    }
    console.log("parksToUpdate:")
    console.dir(parksToUpdate)
    if (Object.keys(parksToUpdate).length === 0) { return }
    this.setState((prevState) => {
      let nodes = prevState.nodes
      for (let parkId in parksToUpdate) {
        for (let node of nodes) {
          if (parkId === node.id) {
            node.isChecked = parksToUpdate[parkId]
          }
        }
      }
      return { nodes }
    })
  }

  getDistanceData = (origin: string) => {
    return this.hardcodedTestData() //
  }

  submitOnClick = () => {
    const origin = this.state.zipCode
    if (this.validateZipCode(origin) === false) {
      console.log("add the fail case here " + origin)
      return
    }
    let distanceData = this.getDistanceData(origin)
    this.setState((prevState) => {
      let parks = distanceData.parks
      let nodes = prevState.nodes
      let originData = distanceData.origin
      let origin = this.calcOriginPosition(originData)
      return { nodes, origin }
    })
  }

  addNode = (id: string, nodeName: string, color: string, xPos: number, yPos: number) => {
    this.setState(prevState => {
      let nodeInfo: NodeInfo = { id: id, name: nodeName, color: color, xPos: xPos, yPos: yPos }
      let nodes = prevState.nodes
      nodes = [...prevState.nodes, nodeInfo]
      return { nodes }
    })
  }

  handleTextInput = (event: any) => {
    console.log(event)
    this.setState({ zipCode: event.target.value })
  }

  validateZipCode = (zipCode: string): boolean => {
    if (typeof (Number(zipCode)) !== "number") {
      return false
    }
    if (zipCode.length !== 5) {
      return false
    }
    return true
  }

  defineBoundaries = (): Boundaries => {
    return {
      north: 47.1,
      south: 42.3,
      east: -86.4,
      west: -93.2,
    }
  }

  definePixelRate = (dimensions: [number, number], boundaries: Boundaries): PixelRates => {
    let ewSpan = boundaries.west - boundaries.east
    let nsSpan = boundaries.north - boundaries.south
    let longPixelRate = dimensions[0] / ewSpan
    let latPixelRate = dimensions[1] / nsSpan
    return { lat: latPixelRate, long: longPixelRate }
  }

  createNodesForParks = (inputData: InputData): NodeInfo[] => {
    let nodes = []
    let dimensions = this.defineDimensions()
    let boundaries = this.defineBoundaries()
    let pixelRates = this.definePixelRate(dimensions, boundaries)
    //
    //go find loop that gets parks out of my dumb data structure
    for (let region in inputData) {
      if (region === 'allChecked') { continue }
      for (let park of inputData[region]['parkList']) {
        let coordinates = this.calcParkPosition(park, boundaries, pixelRates)
        let node = {
          id: park.id,
          name: park.name,
          color: this.getRegionColor(region),
          xPos: coordinates[0],
          yPos: coordinates[1],
          region: region,
          isChecked: park.isChecked,
        }
        nodes.push(node)
      }
    }
    return nodes
  }

  calcParkPosition = (park: Park, boundaries: Boundaries, pixelRate: PixelRates): [number, number] => {
    let xPos = boundaries.west - park.lng
    let yPos = boundaries.north - park.lat
    return [xPos * pixelRate.long, yPos * pixelRate.lat]
  }

  calcOriginPosition = (origin: Park): NodeInfo => {
    let dimensions = this.defineDimensions()
    let boundaries = this.defineBoundaries()
    let pixelRates = this.definePixelRate(dimensions, boundaries)
    let coordinates = this.calcParkPosition(origin, boundaries, pixelRates)
    return {
      id: '0',
      name: origin.name,
      xPos: coordinates[0],
      yPos: coordinates[1],
      color: 'FFFFFF',
    }
  }

  defineDimensions = (): [number, number] => {
    return [1000, 1000]
  }

  getRegionColor = (regionName: string): string => {
    let color = "FFFFFF"
    switch (regionName) {
      case ("northwest"):
        color = "#fad87b"
        break
      case ("northeast"):
        color = "#b1d5bc"
        break
      case ("southwest"):
        color = "#bcd682"
        break
      case ("southeast"):
        color = "#ffca6e"
        break
      default:
        color = "#FFFFFF"
    }
    return color
  }

  _handleKeyDown = (e: any) => {
    if (e.key === 'Enter') {
      this.submitOnClick()
    }
  }

  handleChange = (e, regionName: string) => {
    let name = e.target.name
    let checked = e.target.checked
    this.setState((prevState) => {
      let nodes = prevState.nodes
      nodes = nodes.map(item => item.name === name ? { ...item, isChecked: checked } : item);
      return { nodes }
    })
    this.props.handleChange(e, regionName)
  }

  render() {
    return (
      <div>
        <label>Starting Zip Code:</label>
        <input type="text" id="zipCode" placeholder="Zip Code" onChange={this.handleTextInput} onKeyDown={this._handleKeyDown}></input>
        <Button text="Submit ZIP" onClick={this.submitOnClick} />
        < MapBody nodes={this.state.nodes} origin={this.state.origin} handleChange={this.handleChange} />
      </div>
    );
  }


  hardcodedTestData = (): ServerDistanceData => {
    return {
      'origin': {
        'id': 0,
        'isChecked': false,
        'name': '53703',
        'lat': 43.07,
        'lng': -89.37,
      },
      'parks': {
        '1': {
          'distance': '312 mi',
          'time': '4 hours 43 mins'
        },
        '24': {
          'distance': '28.0 mi',
          'time': '34 mins'
        },
        '3': {
          'distance': '332 mi',
          'time': '6 hours 24 mins'
        },
        '4': {
          'distance': '76.2 mi',
          'time': '1 hour 31 mins'
        },
        '43': {
          'distance': '126 mi',
          'time': '2 hours 1 min'
        },
        '42': {
          'distance': '31.6 mi',
          'time': '36 mins'
        },
        '7': {
          'distance': '317 mi',
          'time': '4 hours 54 mins'
        },
        '37': {
          'distance': '199 mi',
          'time': '3 hours 17 mins'
        },
        '46': {
          'distance': '84.8 mi',
          'time': '1 hour 28 mins'
        },
        '10': {
          'distance': '52.0 mi',
          'time': '1 hour 3 mins'
        },
      }
    }
  }

}

export default Map;
