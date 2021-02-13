import React from 'react'
import AdhocRegion from './adhocRegion'
import AdhocRow from './adhocRow'
import Region from './region'

class AdhocResults extends React.Component {
    render() {
        let css = "adhoc-results"
        if (this.props.status != true) {
            return (
                <div></div>
            )
        }
        else if (this.props.adhocResults.length == 0) {
            return (
                <div className={css}>
                    Unfortunately, no campsites are available for the parks
                    you selected. Some parks have minimum and maximum stay
                    restrictions, so make sure you are selecting appropriate
                    dates. </div>
            )
        }
        else {
            return (
                <div className={css}>
                    <div>Good news! Here are the parks that are available for the dates you selected:</div>
                    {this.props.adhocResults.map((region, index1) => (
                        <div>
                            <AdhocRow text={region.name} additionalCss="adhoc-row-header" />
                            <AdhocRegion regionInfo={region.parks} />
                        </div>
                    ))}
                </div>
            )
        }
    }
}

export default AdhocResults