import React from 'react';
import DateRangePicker from "./DateRangePicker"
import Map from "./compiledTS/Map"
import { DateUtils } from 'react-day-picker';
import ParkSelector from "./parkCheckboxes"
import LoadingIndicator from "./loadingIndicator"
import AdhocResults from "./adhocResults"
import { trackPromise } from 'react-promise-tracker'
import clone from '../scripts/clone'
import Button from './compiledTS/resources/Button';
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
          let loggedIn = data['loggedIn']
          let parks = prevState['parks']
          for (let regionName in data['regions']) {
            prevState['regions'][regionName] = data['regions'][regionName]['id']
            parks[regionName]["link"] = data['regions'][regionName]['link']
            parks[regionName]['parkList'] = this.convertParksToList(data['regions'][regionName]["parks"])
          }
          let initialLoading = false
          return { loggedIn, parks, initialLoading }
        })
      })
    return
  }

  convertParksToList = (parkObj) => {
    let returnList = []
    for (let parkName in parkObj) {
      returnList.push(this.stateItem(parkObj[parkName]['id'], parkName, parkObj[parkName]['lat'], parkObj[parkName]['lng']))
    }
    return returnList
  }

  stateItem = (id, parkName, lat, lng) => {
    return (
      {
        id: id, name: parkName, isChecked: false, lat: lat, lng: lng
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
    regions: {},
    from: null,
    to: null,
    success: null,
    successMessage: null,
    error: { bannerLocation: null, message: null },
    adhocResults: [],
    adhocSuccess: null,
    adhocRegionCount: 0,
    adhocRegionsReturned: 0,
    initialLoading: true,
    origin: {},
    loggedIn: false,
    zipCode: null,
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
      let parks = {}
      clone(parks, prevState['parks'])
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

  handleSelectAllButtonClick = (e, checked) => {
    this.setState(prevState => {
      let parks = {}
      clone(parks, prevState['parks'])
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

  setErrorState = (errorMessage, bannerLocation) => {
    this.setState(prevState => {
      prevState.success = false
      prevState.error = { bannerLocation: bannerLocation, message: errorMessage }
      return prevState
    })
  }

  validateDatesForSubmit = () => {
    if (this.state.from === null) {
      this.setErrorState("Please enter a start date!", "bottom")
      return
    }

    if (this.state.to === null) {
      this.setErrorState("Please enter an end date!", "bottom")
      return
    }

    var today = new Date()
    var tomorrow = new Date()
    today.setHours(0, 0, 0, 0)
    tomorrow.setDate(tomorrow.getDate() + 1)
    tomorrow.setHours(0, 0, 0, 0)

    if (this.state.from < today) {
      this.setErrorState("Start date must be today or later!", "bottom")
      return
    }

    if (this.state.to < tomorrow) {
      this.setErrorState("End date must be tomorrow or later!", "bottom")
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
      this.setErrorState("There is an issue with the Region selection. Please re-select and try again.", "bottom")
      return
    }
    return preferredRegions
  }

  validateParksForSubmit = () => {
    let parks = this.assembleParks()
    if (parks === undefined) {
      this.setErrorState("There is an issue with the Park list. Please re-select and try again.", "bottom")
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
      this.setErrorState("Please select some parks!", "bottom")
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

    //get the count of regions outside the async loop
    for (let region in parks) {
      this.setState(prevState => {
        prevState.adhocRegionCount++
        return prevState
      })
    }

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
              if (data.adhocResults.parks.length > 0) { prevState.adhocResults.push(data.adhocResults) }
              prevState.adhocRegionsReturned++
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
      this.setState(prevState => {
        prevState.success = true
        prevState.successMessage = "Search Submitted!"
        return prevState
      })
    })
  }

  resetAdhocSearch() {
    this.resetErrorState()
    this.setState(prevState => {
      prevState.adhocResults = []
      prevState.adhocSuccess = null
      prevState.adhocRegionCount = 0
      prevState.adhocRegionsReturned = 0
      return prevState
    })
  }

  resetErrorState() {
    this.setState(prevState => {
      prevState.error = { bannerLocation: null, message: null }
      prevState.success = null
      prevState.successMessage = null
      return prevState
    })
  }

  resetOrigin() {
    this.setState(prevState => {
      origin = {}
      return { origin }
    })
  }

  _handleKeyDown = (e) => {
    if (e.key === 'Enter') {
      this.submitOnClick()
    }
  }

  handleTextInput = (event) => {
    this.setState({ zipCode: event.target.value })
  }


  submitOnClick = () => {
    this.resetErrorState()
    this.resetOrigin()
    const origin = this.state.zipCode
    if (origin === undefined) {
      return
    }

    if (this.validateZipCode(origin) === false) {
      this.setErrorState(this.state.zipCode + " is not a valid zip code", "zip")
      return
    }
    let distanceData = this.getDistanceData(origin)
    this.processDistanceData(distanceData)
  }


  getDistanceData = (zip) => {
    //return this.hardcodedTestData()
    fetch('_load_distances_from_origin', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      cache: 'no-cache',
      body: JSON.stringify({
        'zip': zip,
      }),
    })
      .then(response => response.json())
      .then(data => {
        if (data.error) {
          this.setErrorState(data.error, "zip")
          return
        }
        this.processDistanceData(data)
      })
  }

  processDistanceData = (serverData) => {
    if (serverData === undefined) {
      return
    }
    this.setState((prevState) => {
      let origin = []
      let parks = {}
      clone(origin, prevState['origin'])
      clone(parks, prevState['parks'])

      origin = serverData['origin']

      for (let region in parks) {
        if (region === 'allChecked') { continue }
        for (let park of parks[region]['parkList']) {
          if (park.id in serverData['parks']) {
            park.distance = serverData['parks'][park.id]['distance']
            park.time = serverData['parks'][park.id]['time']
          }
        }
      }

      return { origin, parks }

    })
  }


  validateZipCode = (zipCode) => {
    if (typeof (Number(zipCode)) !== "number") {
      return false
    }
    if (zipCode.length !== 5) {
      return false
    }
    return true
  }


  getInitialState() {
    return {
      from: null,
      to: null,
    };
  }

  render() {
    let bottomBanner = ""
    let zipErrBanner = ""
    let map = <div></div>
    let scheduleSearchButton = ""
    let buttonHelpText = ""
    if (this.state.success === true) {
      bottomBanner = <div className="successBanner">{this.state.successMessage}</div>
    }
    if (this.state.success === false && this.state.error.bannerLocation === 'zip') {
      zipErrBanner = <div className="errorBanner">{this.state.error.message}</div>
    }
    if (this.state.success === false && this.state.error.bannerLocation === 'bottom') {
      bottomBanner = <div className="errorBanner">{this.state.error.message}</div>
    }
    if (this.state.initialLoading === false) {
      map = <div id="svg-map"><Map handleChange={this.handleCheckboxChange} parks={this.state.parks} origin={this.state.origin} /></div>
    }
    if (this.state.loggedIn === true) {
      scheduleSearchButton = <button className="submitButton" onClick={this.handleSubmit} title="Add these search criteria to the background search process">Schedule Search</button>
      buttonHelpText = <span className="help-tip">
        <span className="help-tip-text">
          Which button should I choose?
        </span>
        <p>Submitting the search is useful if you want to get notified by email or text when
          there is a campsite available for the dates and parks you selected.
          Instascraping is for when you want to check if anything
          is available for your parks and dates in real time. Caveat:
          Instascrape is a little inconsistent and can take a few minutes. If you
          don't get results the first time, try again!</p>
      </span>
    }

    return (<div>
      <div className="form-block">
        <div className="form-header">Choose the parks you would like to stay at:</div>
        {map}
        <ParkSelector
          handleCheckboxChange={this.handleCheckboxChange}
          handleSelectAllButtonClick={this.handleSelectAllButtonClick}
          parks={this.state.parks}
        />
      </div>
      <div className="form-block">
        <div className="form-header">Enter a Zip Code to get time and distance info: </div>
        <input type="text" id="zipCode" placeholder="Zip Code" className="zipCodeInput" onChange={this.handleTextInput} onKeyDown={this._handleKeyDown}></input>
        <Button text="Submit ZIP" onClick={this.submitOnClick} />
        {zipErrBanner}
      </div>
      <div className="form-block">
        <div className="form-header">Choose the dates you would like to camp:</div>
        <div>For use with the scraper that looks for campsite availability</div>
        <DateRangePicker handleDayClick={this.handleDayClick} handleResetClick={this.handleResetClick} from={this.state.from} to={this.state.to} />
      </div>
      <div>
        {scheduleSearchButton}
        <button className="instascrapeButton" onClick={this.handleSubmitAdhoc} title="Search now for these criteria and get results in real time">InstaScrape</button>
        {buttonHelpText}
      </div>
      {bottomBanner}
      < LoadingIndicator message="Scraping in progress...Results will load as
      they become available, but this can take a minute or two to complete.
      Please don't navigate away from this page." />
      < AdhocResults
        status={this.state.adhocSuccess}
        adhocResults={this.state.adhocResults}
        regionCount={this.state.adhocRegionCount}
        regionResults={this.state.adhocRegionsReturned}
      />
    </div>)
  }
}


export default Form;