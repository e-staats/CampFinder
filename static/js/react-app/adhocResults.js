import React from 'react'
import AdhocRow from './adhocRow'

class AdhocResults extends React.Component {
    render() {
        let css = "adhoc-results"
        if (this.props.adhocResults === null) {
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
                    <div className="successBanner">Good news! Here are the parks that are available for the dates you selected:</div>
                    {this.props.adhocResults.map((result, index) => (
                        <AdhocRow additionalCss="adhoc-row"
                            val1={result.name}
                            val2={result.url} />
                    ))}
                </div>
            )
        }
    }
}

export default AdhocResults