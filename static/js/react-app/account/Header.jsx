import React from 'react';

class Header extends React.Component {
    handleToggleClick = (e, id) => {
        return this.props.handleToggleClick(e, id)
    }

    render() {
        return (
            <div className="row table-header">
            <div className="col-sm-2 row-item">Start Date</div>
            <div className="col-sm-2 row-item">End Date</div>
            <div className="col-sm-2 row-item">Region Pref.</div>
            <div className="col-sm-2 row-item">Addt'l Parks</div>
            <div className="col-sm-1 row-item">Active?</div>
            <div className="col-sm-2 row-item">Submitted on</div>
            <div className="col-sm-1 row-item"></div>
        </div>
        )
    }
}


export default Header;