import React from 'react';

class Header extends React.Component {
    handleToggleClick = (e, id) => {
        return this.props.handleToggleClick(e, id)
    }

    render() {
        return (
            <div className="row table-header">
            <div className="col-sm-2">Start Date</div>
            <div className="col-sm-2">End Date</div>
            <div className="col-sm-2">Region Preference</div>
            <div className="col-sm-2">Additional Selected Parks</div>
            <div className="col-sm-1">Active?</div>
            <div className="col-sm-2">Submitted Date</div>
            <div className="col-sm-1"></div>
        </div>
        )
    }
}


export default Header;