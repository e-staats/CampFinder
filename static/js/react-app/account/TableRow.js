import React from 'react';
import NameList from './NameList'
import ToggleSwitch from './ToggleSwitch'

class TableRow extends React.Component {
    handleToggleClick = (e, id) => {
        return this.props.handleToggleClick(e, id)
    }

    render() {
        let style = "inactive"
        let isActive = "No"
        if (this.props.search.is_active === true) {
            style = "active"
            isActive = "Yes"
        }
        let rowClass = "row table-row " + style

        return (
            <div id={this.props.search.id} className={rowClass}>
                <div className="col-sm-2">{this.props.search.start_date}</div>
                <div className="col-sm-2">{this.props.search.end_date}</div>
                <div className="col-sm-2">< NameList list={this.props.search.region_names} /></div>
                <div className="col-sm-2">< NameList list={this.props.search.park_names} /></div>
                <div className="col-sm-1">{isActive}</div>
                <div className="col-sm-2">{this.props.search.submit_instant}</div>
                <div className="col-sm-1">< ToggleSwitch is_active={this.props.search.is_active} id={this.props.search.id} handleToggleClick={this.handleToggleClick} /></div>
            </div>
        )
    }
}


export default TableRow;