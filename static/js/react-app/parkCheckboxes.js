import Region from "./region"
import React, { Component } from "react"

class ParkSelector extends Component {

    handleSelectAllButtonClick = (e) => {
        this.props.handleSelectAllButtonClick(e)
        console.log("heyo")
    }

    regionClassName = (name) => {
        return ('col-md-3 ' + name)

    }
    render() {
        return (

            <div className="checkboxes">
                <div className='row'>
                    <div className='masterButton'>
                        <button type="button" name="checkAll" onClick={this.handleSelectAllButtonClick} className="btn btn-primary">
                            Check All
                    </button>
                    </div>
                    <div className='masterButton'>
                        <button type="button" name="uncheckAll" onClick={this.handleSelectAllButtonClick} className="btn btn-danger">
                            Uncheck All
                        </button>
                    </div>
                </div>
                <div className='row'>
                    <div className={this.regionClassName(this.props.parks.northwest.name)}>
                        < Region name={this.props.parks.northwest.name} parkList={this.props.parks.northwest.parkList} allChecked={this.props.parks.northwest.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.northeast.name)}>
                        < Region name={this.props.parks.northeast.name} parkList={this.props.parks.northeast.parkList} allChecked={this.props.parks.northeast.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.southeast.name)}>
                        < Region name={this.props.parks.southeast.name} parkList={this.props.parks.southeast.parkList} allChecked={this.props.parks.southeast.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.southwest.name)}>
                        < Region name={this.props.parks.southwest.name} parkList={this.props.parks.southwest.parkList} allChecked={this.props.parks.southwest.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                </div>
            </div>
        )
    }
}

export default ParkSelector