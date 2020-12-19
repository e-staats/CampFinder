import React from 'react';

class Checkbox extends React.Component {
    handleChange = (e) => {
        return this.props.handleCheckboxClick(e)
    }

    render() {
        return (
            <input
                type="checkbox"
                className="preference-checkbox"
                name={this.props.name}
                checked={this.props.checked}
                onChange={this.handleChange}
            />
        )
    }
}


export default Checkbox;