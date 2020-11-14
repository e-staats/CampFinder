import React from 'react';

class NameList extends React.Component {
    render() {
        return (
            <ul>
                {this.props.list.map((item, index) => (
                    <li>{item}</li>
                )
                )}
            </ul>
        )
    }
}


export default NameList;