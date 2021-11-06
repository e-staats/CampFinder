import React from 'react'

class AdhocRow extends React.Component {
    render() {
        let css = this.props.additionalCss
        if (this.props.url === undefined) {
            return (
                <div className={css}>{this.props.text}</div>
            )
        }
        else {
            return (
                <div className={css}><a href={this.props.url}>{this.props.text}</a></div>
            )
        }
    }
}

export default AdhocRow