import React from 'react';
import DateRangePicker from "./DateRangePicker"
import { DateUtils } from 'react-day-picker';
import ParkSelector from "./parkCheckboxes"

class Form extends React.Component {
  northwest = [
    "Amnicon Falls",
    "Big Bay",
    "Brule River",
    // "Brunet Island",
    // "Chippewa Flowage",
    // "Chippewa Moraine",
    // "Copper Falls",
    // "Flambeau River",
    // "Governor Knowles",
    // "Interstate",
    // "Lake Wissota",
    // "Pattison",
    // "Straight Lake",
    // "Turtle Flambeau",
    // "Willow River",
  ]

  northeast = [
    "Council Grounds",
    "Governor Earl Peshtigo River",
    "Governor Thompson",
    // "Hartman Creek",
    // "High Cliff",
    // "Menominee River",
    // "Newport",
    // "Northern Highland - American Legion",
    // "Peninsula",
    // "Point Beach",
    // "Potawatomi",
    // "Rib Mountain",
    // "Rock Island",
    // "Whitefish Dunes",
    // "Willow Flowage",
  ]

  southeast = [
    "Black River",
    "Blue Mound",
    "Buckhorn",
    // "Cadiz Springs",
    // "Devil",
    // "Elroy-Sparta",
    // "Governor Dodge",
    // "Governor Nelson",
    // "Lake Kegonsa",
    // "Mackenzie Center",
    // "Merrick",
    // "Mill Bluff",
    // "Mirror Lake",
    // "Nelson Dewey",
    // "New Glarus Woods",
    // "Perrot",
    // "Roche-A-Cri",
    // "Rocky Arbor",
    // "Tower Hill",
    // "Wildcat Mountain",
    // "Wyalusing",
    // "Yellowstone Lake",
  ]

  southwest = [
    "Aztalan",
    "Big Foot Beach",
    "Glacial Drumlin",
    // "Harrington Beach",
    // "Kettle Moraine - Lapham Peak Unit",
    // "Kettle Moraine - Northern Unit",
    // "Kettle Moraine - Pike Lake Unit",
    // "Kettle Moraine - Southern Unit",
    // "Kohler-Andrae",
    // "Lakeshore",
    // "Richard Bong",
  ]

  stateItem = (id, parkName) => {
    return (
      {
        id: id, name: parkName, isChecked: false,
      }
    )
  }

  state = {
    parks: {
      allChecked: true,
      northwest: {
        name: "northwest",
        allChecked: false,
        parkList: this.northwest.map((parkName, index) => this.stateItem(index, parkName)),
      },
      southwest: {
        name: "southwest",
        allChecked: false,
        parkList: this.southwest.map((parkName, index) => this.stateItem(index, parkName)),
      },
      northeast: {
        name: "northeast",
        allChecked: false,
        parkList: this.northeast.map((parkName, index) => this.stateItem(index, parkName)),
      },
      southeast: {
        name: "southeast",
        allChecked: false,
        parkList: this.southeast.map((parkName, index) => this.stateItem(index, parkName)),
      },
    },
    regions: ["northwest", "northeast", "southwest", "southeast"],
    from: undefined,
    to: undefined,
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

  handleSelectAllButtonClick = e => {
    let checked
    e.target.name === "checkAll" ? checked = true : checked = false
    this.setState(prevState => {
      let parks = prevState['parks']
      let regionName
      for (regionName of prevState["regions"]) {
        parks = this.updateAllRegionalCheckboxes(parks, regionName, checked)
      }
      return { parks };
    })
  };

  handleSubmit = e => {
    console.log(e)
    alert("you clicked submit")
  }

  getInitialState() {
    return {
      from: undefined,
      to: undefined,
    };
  }

  render() {
    return (<form>
      <div>
        <h3>Choose the dates you would like to camp:</h3>
        <DateRangePicker handleDayClick={this.handleDayClick} handleResetClick={this.handleResetClick} from={this.state.from} to={this.state.to} />
      </div>
      <div>
        <h3>Choose the parks you would like to stay at:</h3>
        <ParkSelector
          handleCheckboxChange={this.handleCheckboxChange}
          handleSelectAllButtonClick={this.handleSelectAllButtonClick}
          parks={this.state.parks}
        />
      </div>
      <button className="btn btn-success" onClick={this.handleSubmit}>Submit</button>
    </form>)
  }
}


export default Form;