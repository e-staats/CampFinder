import React from 'react';
import TableRow from './TableRow';
import Header from './Header';

class SearchTable extends React.Component {
    state = { searchList: null }

    componentDidMount() {
        this.fetchData()
    }

    fetchData = () => {
        fetch('/account/_load_search_list', {
            method: 'GET', // *GET, POST, PUT, DELETE, etc.
            headers: {
                'Content-Type': 'application/json'
            },
        })
            .then(response => response.json())
            .then(data => {
                this.setState(prevState => {
                    prevState.searchList = data.searchList
                    return prevState
                })
            })
        return
    }

    handleToggleClick = (e, id) => {
        this.setState(prevState => {
            let searchList = prevState.searchList

            searchList = searchList.map(item => this.toggleItem(id, item));

            return { searchList }
        })
    }

    toggleItem = (id, item) => {
        if (item.id === id) {
            item.is_active = !item.is_active
            this.postToggle(id, item.is_active)
        }
        return item
    }

    postToggle = (id, status) => {
        //call down to server
        fetch('/account/_toggle_search_status', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            cache: 'no-cache',
            body: JSON.stringify({
                'id': id,
                'is_active': status,
            }),
        })
    }

    render() {
        if (this.state.searchList === null) {
            return (
                <div>
                    You have no submitted searches at this time.
                </div>
            )
        }
        else if (this.state.searchList != null) {
            let locale = window.navigator.userLanguage || window.navigator.language;
            return (
                <div>
                    <Header />
                    {this.state.searchList.map((search, index) => (
                        <TableRow search={search} handleToggleClick={this.handleToggleClick} locale={locale}/>
                    )
                    )}
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


export default SearchTable;