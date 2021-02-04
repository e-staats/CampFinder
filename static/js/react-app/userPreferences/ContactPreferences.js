import React from 'react';
import Checkbox from './checkbox'

class ContactPreferences extends React.Component {
    handleCheckboxClick = (e) => {
        return this.props.handleCheckboxClick(e)
    }

    render() {
        return (
            <div>
                <div className="preference-header">Contact Preferences:</div>
                <Checkbox name="email" checked={this.props.emailChecked} handleCheckboxClick={this.props.handleCheckboxClick} label="Receive Email Notifications?" />
                <Checkbox name="text" checked={this.props.textChecked} handleCheckboxClick={this.props.handleCheckboxClick} label="Receive Text Notifications? [coming soon!]" />
            </div>
        )
    }
}


export default ContactPreferences;