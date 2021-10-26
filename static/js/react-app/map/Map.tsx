import React from 'react';
import MapBody from './resources/MapBody';

export interface Props {
  handleChange(arg1: React.ChangeEvent<HTMLInputElement>, arg2: string): any,
  parks: InputData,
  origin?: Park,
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
  id: number,
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
  originNode: NodeInfo,
}

class Map extends React.Component<Props, State> {
  constructor(props: Props) {
    super(props)
    this.state = {
      nodes: [],
      zipCode: "",
      originNode: {
        id: 0,
        name: 'undefined',
        color: 'FFFFFF',
        xPos: 0,
        yPos: 0,
      }
    }
  }

  componentDidMount() {
    this.setState(() => {
      let nodes = this.createNodesForParks(this.props.parks)
      return { nodes }
    })
  }

  componentDidUpdate(prevProps) {
    if (this.props.parks !== prevProps.parks) {
      this.updateNodeCheckedStatus(this.props.parks, prevProps.parks)
    }
    if (this.props.origin !== prevProps.origin) {
      this.updateOrigin(this.props.origin)
    }
  }

  updateNodeCheckedStatus = (parks: InputData, prevParks: InputData) => {
    //Because the data structures are pretty weird, this is a two parter: get
    //the list of parks to update, then go through and update the nodes
    let parksToUpdate: { [id: number]: boolean } = {}
    for (let region in parks) {
      if (region === 'allChecked') { continue }
      for (let park of parks[region]['parkList']) {
        for (let prevPark of prevParks[region]['parkList']) {
          if (park.isChecked !== prevPark.isChecked) {
            parksToUpdate[park.id] = park.isChecked
          }
        }
      }
    }
    if (Object.keys(parksToUpdate).length === 0) { return }
    this.setState((prevState) => {
      let nodes = prevState.nodes
      for (let node of nodes) {
        if (node.id in parksToUpdate) {
          node.isChecked = parksToUpdate[node.id]
        }
      }
      return { nodes }
    })
  }

  updateOrigin = (origin: Park) => {
    let dimensions = this.defineDimensions()
    let boundaries = this.defineBoundaries()
    let pixelRates = this.definePixelRate(dimensions, boundaries)
    let coordinates = this.calcParkPosition(origin, boundaries, pixelRates)
    this.setState((prevState) => {
      let originNode = {
        ...prevState.originNode,
        id: 0,
        name: origin.name,
        xPos: coordinates[0],
        yPos: coordinates[1]
      }
      return { originNode }
    })
  }

  addNode = (id: number, nodeName: string, color: string, xPos: number, yPos: number) => {
    this.setState(prevState => {
      let nodeInfo: NodeInfo = { id: id, name: nodeName, color: color, xPos: xPos, yPos: yPos }
      let nodes = prevState.nodes
      nodes = [...prevState.nodes, nodeInfo]
      return { nodes }
    })
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
        < MapBody nodes={this.state.nodes} origin={this.state.originNode} handleChange={this.handleChange} />
      </div>
    );
  }

}

export default Map;
