import React from 'react';

class ToggleSwitch extends React.Component {
    handleToggleClick = (e) => {
        return this.props.handleToggleClick(e, this.props.id)
    }

    render() {
        let text = "Disable"
        let classTitle = "search-disable"
        if (this.props.is_active === false) {
            text = "Enable"
            classTitle = "search-enable"
        }

        return (
            <span className={classTitle} onClick={this.handleToggleClick}>{text}</span>
        )
    }
}


export default ToggleSwitch;