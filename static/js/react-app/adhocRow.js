import React from 'react'

class AdhocRow extends React.Component {
    render() {
        let css = this.props.additionalCss
        return (
            <div className={css}><a href={this.props.val2}>{this.props.val1}</a></div>
        )
    }
}

export default AdhocRow