import React from 'react';
import DateRangePicker from "./DateRangePicker"
import { DateUtils } from 'react-day-picker';
import ParkSelector from "./parkCheckboxes"

class Form extends React.Component {

  componentDidMount() {
    this.fetchData()
  }

  fetchData = () => {
    fetch('/_load_park_data', {
      method: 'GET', // *GET, POST, PUT, DELETE, etc.
      headers: {
        'Content-Type': 'application/json'
      },
    })
      .then(response => response.json())
      .then(data => {
        this.setState(prevState => {
          let parks = prevState['parks']
          for (let regionName in data) {
            prevState['regions'][regionName] = data[regionName]['id']
            parks[regionName]["link"] = data[regionName]['link']
            parks[regionName]['parkList'] = this.convertParksToList(data[regionName]["parks"])
          }
          return { parks }
        })
      })
    return
  }

  convertParksToList = (parkObj) => {
    let returnList = []
    for (let parkName in parkObj) {
      returnList.push(this.stateItem(parkObj[parkName], parkName))
    }
    return returnList
  }

  stateItem = (id, parkName) => {
    return (
      {
        id: id, name: parkName, isChecked: false,
      }
    )
  }

  default_park_state = (name) => {
    return {
      name: name,
      allChecked: false,
      link: "",
      parkList: [],
    }
  }

  state = {
    parks: {
      allChecked: true,
      northwest: this.default_park_state('northwest'),
      southwest: this.default_park_state('southwest'),
      northeast: this.default_park_state('northeast'),
      southeast: this.default_park_state('southeast'),
    },
    //mapping names to values from database:
    regions: {},
    from: undefined,
    to: undefined,
    success: null,
    error: null
  }

  handleDayClick = (day) => {
    const range = DateUtils.addDayToRange(day, this.state);
    this.setState(range);
  }

  handleResetClick = () => {
    this.setState(this.getInitialState());
  }

  updateAllRegionalCheckboxes = (parks, name, checked) => {
    parks[name]["parkList"] = parks[name]["parkList"].map(item => ({ ...item, isChecked: checked }))
    parks[name]['allChecked'] = checked
    return parks
  }

  handleCheckboxChange = (e, name) => {
    let itemName = e.target.name;
    let checked = e.target.checked;
    this.setState(prevState => {
      let parks = prevState['parks']
      switch (itemName) {
        case ("allChecked"):
          parks = this.updateAllRegionalCheckboxes(parks, name, checked)
          break
        default:
          parks[name]['parkList'] = parks[name]['parkList'].map(item =>
            item.name === itemName ? { ...item, isChecked: checked } : item
          );
          parks[name]['allChecked'] = parks[name]['parkList'].every(item => item.isChecked);
      }
      return { parks };
    })
  };

  handleSelectAllButtonClick = (e, checkedOverride = null) => {
    let checked = checkedOverride
    if (checked === null) {
      e.target.name === "checkAll" ? checked = true : checked = false
    }
    this.setState(prevState => {
      let parks = prevState['parks']
      for (let regionName in prevState.regions) {
        parks = this.updateAllRegionalCheckboxes(parks, regionName, checked)
      }
      return { parks };
    })
  };

  assemblePreferredRegions = () => {
    let regionString = ""
    for (let regionName in this.state.regions) {
      if (this.state['parks'][regionName]['allChecked'] === true) {
        regionString += this.state.regions[regionName].toString() + ","
      }
    }
    return regionString
  }

  assembleParkString = () => {
    let parkString = ""
    for (let regionName in this.state.regions) {
      for (let parkObj of this.state['parks'][regionName]['parkList']) {
        if (parkObj.isChecked === true) {
          parkString += parkObj['id'].toString() + ","
        }
      }
    }
    return parkString
  }

  setErrorState = (errorMessage) => {
    this.setState(prevState => {
      prevState.success = false
      prevState.error = errorMessage
      return prevState
    })
  }

  validateDatesForSubmit = () => {
    //validate and assemble data

    if (this.state.from === undefined) {
      this.setErrorState("Please enter a start date!")
      return
    }

    if (this.state.to === undefined) {
      this.setErrorState("Please enter an end date!")
      return
    }

    return {
      from: this.state.from,
      to: this.state.to
    }
  }

  validateRegionsForSubmit = () => {
    //validate and assemble data
    let preferredRegions = this.assemblePreferredRegions()
    if (preferredRegions === undefined) {
      this.setErrorState("There is an issue with the Region selection. Please re-select and try again.")
      return
    }

    return preferredRegions
  }

  validateParksForSubmit = () => {
    //validate and assemble data
    let parkList = this.assembleParkString()
    if (parkList === undefined) {
      this.setErrorState("There is an issure with the Park list. Please re-select and try again.")
      return
    }

    return parkList
  }

  handleSubmit = () => {
    let dates = this.validateDatesForSubmit()
    let regions = this.validateRegionsForSubmit()
    let parks = this.validateParksForSubmit()
    if (dates === undefined || regions === undefined || parks === undefined) {
      return
    }
    if (regions === "" && parks === "") {
      this.setErrorState("Please select some parks!")
      return
    }

    let fromDate = dates.from.toISOString()
    let toDate = dates.to.toISOString()

    //call down to server
    fetch('/_submit_search', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      cache: 'no-cache',
      body: JSON.stringify({
        'start_date': fromDate,
        'end_date': toDate,
        'regions': regions,
        'parks': parks,
      }),
    }).then(() => {
      this.handleSelectAllButtonClick(null, false)
      this.handleResetClick()
      this.setState(prevState => {
        prevState.success = true
        return prevState
      })
    })
  }

  getInitialState() {
    return {
      from: undefined,
      to: undefined,
    };
  }

  render() {
    let banner = ""
    if (this.state.success === true) {
      banner = <div className="successBanner">Search submitted!</div>
    }
    if (this.state.success === false) {
      banner = <div className="errorBanner">{this.state.error}</div>
    }

    return (<div>
      <div className="form-block">
        <div className="form-header">Choose the dates you would like to camp:</div>
        <DateRangePicker handleDayClick={this.handleDayClick} handleResetClick={this.handleResetClick} from={this.state.from} to={this.state.to} />
      </div>
      <div className="form-block">
        <div className="form-header">Choose the parks you would like to stay at:</div>
        <ParkSelector
          handleCheckboxChange={this.handleCheckboxChange}
          handleSelectAllButtonClick={this.handleSelectAllButtonClick}
          parks={this.state.parks}
        />
      </div>
      <div>
        <button className="submitButton" onClick={this.handleSubmit}>Schedule Search</button>
        <button class="instascrapeButton" disabled>InstaScrape (coming soon)</button>
      </div>
      {banner}
    </div>)
  }
}


export default Form;