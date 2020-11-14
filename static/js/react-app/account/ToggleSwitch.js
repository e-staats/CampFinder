import React from 'react';

class ToggleSwitch extends React.Component {
    handleToggleClick = (e) => {
        return this.props.handleToggleClick(e, this.props.id)
    }

    render() {
        let text = "Disable"
        let css = "btn-outline-danger"
        if (this.props.is_active === false) {
            text = "Enable"
            css = "btn-outline-success"
        }
        let classTitle = "btn btn-sm " + css

        return (
            <button type="button" className={classTitle} onClick={this.handleToggleClick}>{text}</button>
        )
    }
}


export default ToggleSwitch;