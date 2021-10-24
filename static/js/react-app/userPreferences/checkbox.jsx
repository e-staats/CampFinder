import React from 'react';

class Checkbox extends React.Component {
    handleChange = (e) => {
        return this.props.handleCheckboxClick(e)
    }

    render() {
        return (
            <label className="preference-checkbox">
                <input
                    type="checkbox"
                    name={this.props.name}
                    checked={this.props.checked}
                    onChange={this.handleChange}
                />
                <span>{this.props.label}</span>
            </label>
        )
    }
}


export default Checkbox;