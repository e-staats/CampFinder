import Region from "./region"
import React, { Component } from "react"

class ParkSelector extends Component {

    handleCheckAllButtonClick = (e) => {
        this.props.handleSelectAllButtonClick(e, true)
    }

    handleUncheckAllButtonClick = (e) => {
        this.props.handleSelectAllButtonClick(e, false)
    }

    regionClassName = (name) => {
        return ('col-md-3 ' + name)
    }

    render() {
        return (

            <div className="checkboxes">
                <div className='row masterButtonArray'>
                        <div className='masterButton'>
                            <span onClick={this.handleCheckAllButtonClick} className="masterCheckAll">
                                Check All
                    </span>
                        </div>
                        <div className='masterButton'>
                            <span onClick={this.handleUncheckAllButtonClick} className="masterUncheckAll">
                                Uncheck All
                        </span>
                        </div>
                </div>
                <div className='row checkboxArray'>
                    <div className={this.regionClassName(this.props.parks.northwest.name)}>
                        < Region name={this.props.parks.northwest.name} link={this.props.parks.northwest.link} parkList={this.props.parks.northwest.parkList} allChecked={this.props.parks.northwest.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.northeast.name)}>
                        < Region name={this.props.parks.northeast.name} link={this.props.parks.northeast.link} parkList={this.props.parks.northeast.parkList} allChecked={this.props.parks.northeast.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.southeast.name)}>
                        < Region name={this.props.parks.southeast.name} link={this.props.parks.southeast.link} parkList={this.props.parks.southeast.parkList} allChecked={this.props.parks.southeast.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                    <div className={this.regionClassName(this.props.parks.southwest.name)}>
                        < Region name={this.props.parks.southwest.name} link={this.props.parks.southwest.link} parkList={this.props.parks.southwest.parkList} allChecked={this.props.parks.southwest.allChecked} handleCheckboxChange={this.props.handleCheckboxChange} />
                    </div>
                </div>
            </div>
        )
    }
}

export default ParkSelector