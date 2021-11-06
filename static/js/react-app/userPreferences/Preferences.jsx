import React from 'react'
import ContactPreferences from "./ContactPreferences"

class Preferences extends React.Component {
    state = { preferences: null }

    componentDidMount() {
        this.fetchData()
    }

    fetchData = () => {
        fetch('/account/_load_user_preferences', {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                this.setState(prevState => {
                    prevState.preferences = data
                    return prevState
                })
            })
        return
    }

    handleCheckboxClick = (e) => {
        let settingName = e.target.name;
        this.setState(prevState => {
            let preferences = prevState.preferences

            preferences[settingName] = !preferences[settingName]
            this.postCheckboxChange(settingName, preferences[settingName])

            return { preferences }
        })
    }

    postCheckboxChange = (settingName, checked) => {
        //call down to server
        fetch('/account/_toggle_setting_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            cache: 'no-cache',
            body: JSON.stringify({
                'setting': settingName,
                'is_checked': checked,
            }),
        })
    }

    render() {
        if (this.state.preferences === null) {
            return (
                <div>
                    Loading preferences...
                </div>
            )
        }
        else if (this.state.preferences != null) {
            return (
                <div>
                    <ContactPreferences
                        emailChecked={this.state.preferences.email}
                        textChecked={this.state.preferences.text}
                        handleCheckboxClick={this.handleCheckboxClick}
                    />
                </div>
            )
        }
        else {
            return (
                <div></div>
            )
        }
    }

}

export default Preferences