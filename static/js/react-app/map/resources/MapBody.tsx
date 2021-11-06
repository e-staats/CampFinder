import React from 'react';
import Node from './Node';
import { NodeInfo } from '../Map'

export interface Props {
  nodes: NodeInfo[],
  origin: NodeInfo,
  handleChange(arg1: React.ChangeEvent<HTMLInputElement>, arg2: string): any,
}

class MapBody extends React.Component<Props> {

  handleChange = (e, regionName: string) => {
    return this.props.handleChange(e, regionName)
  }

  render() {
    let origin
    if (this.props.origin.name !== 'undefined') {
      origin = <Node item={this.props.origin} />
    }
    else {
      origin = <div></div>
    }

    return (
      <div>
        <div className="container">
          {origin}
          {this.props.nodes.map((info: NodeInfo, index: number) => (
            <Node item={info} handleChange={this.handleChange}/>
          ))}
        </div>
      </div>
    );
  }
}

export default MapBody;
