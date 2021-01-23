import React from 'react';
import DateRangePicker from "./DateRangePicker"
import { DateUtils } from 'react-day-picker';
import ParkSelector from "./parkCheckboxes"
import LoadingIndicator from "./loadingIndicator"
import AdhocResults from "./adhocResults"
import { trackPromise } from 'react-promise-tracker'

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
    from: null,
    to: null,
    success: null,
    successMessage: null,
    error: null,
    adhocResults: [],
    adhocSuccess: null,
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

  assembleParkString = (regionName) => {
    let parkString = ""
    for (let parkObj of this.state['parks'][regionName]['parkList']) {
      if (parkObj.isChecked === true) {
        parkString += parkObj['id'].toString() + ","
      }
    }
    return parkString
  }

  assembleParks = () => {
    let parks = {}
    for (let regionName in this.state.regions) {
      let park_string = this.assembleParkString(regionName)
      if (park_string != "") {
        let region_id = this.state.regions[regionName]
        parks[region_id] = park_string
      }
    }
    return parks
  }

  setErrorState = (errorMessage) => {
    this.setState(prevState => {
      prevState.success = false
      prevState.error = errorMessage
      return prevState
    })
  }

  validateDatesForSubmit = () => {
    if (this.state.from === null) {
      this.setErrorState("Please enter a start date!")
      return
    }

    if (this.state.to === null) {
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
    let parks = this.assembleParks()
    if (parks === undefined) {
      this.setErrorState("There is an issue with the Park list. Please re-select and try again.")
      return
    }
    return parks
  }

  handleSubmitAdhoc = () => {
    this.handleSubmit(true)
  }

  handleSubmit = (adhoc) => {
    let dates = this.validateDatesForSubmit()
    let parks = this.validateParksForSubmit()
    if (dates === undefined || parks === undefined) {
      return
    }
    if (Object.keys(parks).length === 0) {
      this.setErrorState("Please select some parks!")
      return
    }

    let fromDate = dates.from.toISOString()
    let toDate = dates.to.toISOString()

    if (adhoc == true) {
      this.submitSearchAdhoc(fromDate, toDate, parks)
    }
    else {
      this.submitSearchDB(fromDate, toDate, parks)
    }
  }

  async submitSearchAdhoc(fromDate, toDate, parks) {
    this.resetAdhocSearch()

    for (let region in parks) {
     await trackPromise(
        fetch('/_adhoc_search', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          cache: 'no-cache',
          body: JSON.stringify({
            'start_date': fromDate,
            'end_date': toDate,
            'region': region,
            'parks': parks[region],
          }),
        }).then(response => response.json())
          .then(data => {
            this.setState(prevState => {
              prevState.adhocSuccess = true
              if (data.adhocResults.parks.length > 0) {prevState.adhocResults.push(data.adhocResults)}
              return prevState
            })
          })
      )
    }
  }

  submitSearchDB = (fromDate, toDate, parks) => {
    let regions = this.validateRegionsForSubmit()
    if (regions === undefined) {
      return
    }

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
        prevState.successMessage = "Search Submitted!"
        return prevState
      })
    })
  }

  resetAdhocSearch() {
    this.setState(prevState => {
      prevState.error = null
      prevState.adhocResults = []
      prevState.adhocSuccess = null
      return prevState
    })
  }

  getInitialState() {
    return {
      from: null,
      to: null,
    };
  }

  render() {
    let banner = ""
    if (this.state.success === true) {
      banner = <div className="successBanner">{this.state.successMessage}</div>
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
        <button className="instascrapeButton" onClick={this.handleSubmitAdhoc}>InstaScrape</button>
      </div>
      {banner}
      < LoadingIndicator message="Scraping in progress...Results will load as
      they become available, but this can take a minute or two to complete.
      Please don't navigate away from this page." /> < AdhocResults
      status={this.state.adhocSuccess} adhocResults={this.state.adhocResults}
      />
    </div>)
  }
}


export default Form;