import React from 'react'
import AdhocRow from './adhocRow'

class AdhocRegion extends React.Component {
    render() {
        if (this.props.regionInfo === undefined) {
            return <div>Error retrieving park info</div>
        }
        return (
            <div>
                {
                    this.props.regionInfo.map((result, index2) => (
                        <AdhocRow additionalCss="adhoc-row"
                            text={result.name}
                            url={result.url} />
                    ))
                }
            </div>
        )
    }
}

export default AdhocRegion