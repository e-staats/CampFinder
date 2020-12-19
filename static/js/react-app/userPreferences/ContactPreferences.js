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
                <Checkbox name="email" checked={this.props.emailChecked} handleCheckboxClick={this.props.handleCheckboxClick}/>
                Receive Email Notifications?
                <br></br>
                <Checkbox name="text" checked={this.props.textChecked} handleCheckboxClick={this.props.handleCheckboxClick}/>
                Receive Text Notifications? [coming soon!]
            </div>
        )
    }
}


export default ContactPreferences;