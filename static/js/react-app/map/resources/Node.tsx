import React, { CSSProperties } from 'react'
import { NodeInfo } from '../Map'

interface Props {
    item: NodeInfo,
    handleChange?(arg1: React.ChangeEvent<HTMLInputElement>, arg2: string): any,
}

class Node extends React.Component<Props> {

    handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
        let regionName = this.props.item.region
        return this.props.handleChange(e, regionName)
    }

    render() {
        let style: CSSProperties = {
            backgroundColor: this.props.item.color,
            transform: "translate(" + this.props.item.xPos.toString() + "px," + this.props.item.yPos.toString() + "px)"
        }

        if (typeof (this.props.handleChange) === 'undefined') {
            return (
                <div className="origin-circle" style={style}>
                    <span>{this.props.item.name}</span>
                </div>
            )
        }
        return (
            <div>
                <label className="map-circle-checkbox" style={style} >
                    <input
                        key={this.props.item.id}
                        type="checkbox"
                        name={this.props.item.name}
                        value={this.props.item.name}
                        checked={this.props.item.isChecked}
                        onChange={this.handleChange}
                    />
                    <span>{this.props.item.name}</span>
                </label>
            </div>
        )
    }
}

export default Node