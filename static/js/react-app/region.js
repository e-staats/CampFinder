import React, { Component } from "react";

class Region extends Component {
    handleChange = (e) => {
        this.props.handleCheckboxChange(e, this.props.name)
    };

    toCapitalCase = (word) => {
        let firstLetter = word.charAt(0).toUpperCase()
        return (firstLetter + word.slice(1))
    }

    renderList = () => {
        return this.props.parkList.map(item => (
            <div className="parkList">
                <input
                    key={item.id}
                    type="checkbox"
                    name={item.name}
                    value={item.name}
                    checked={item.isChecked}
                    onChange={this.handleChange}
                />
                <label>{item.name}</label>
            </div>
        ));
    };
    render() {
        return (

            <div>
                <div className="region-header"><a href={this.props.link} target="_blank">{this.toCapitalCase(this.props.name)}</a></div>
                <div className="checkAll">
                    <input
                        type="checkbox"
                        name="allChecked"
                        checked={this.props.allChecked}
                        onChange={this.handleChange}
                    />
                    <label>Check all</label>
                </div>
                <div>
                    {this.renderList()}
                </div>
            </div>
        );
    }
}

export default Region