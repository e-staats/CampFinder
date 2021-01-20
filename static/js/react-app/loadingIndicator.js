import React from 'react'
import { usePromiseTracker } from "react-promise-tracker"
import Loader from 'react-loader-spinner'

const LoadingIndicator = props => {
    const { promiseInProgress } = usePromiseTracker();
    return (
        promiseInProgress && <div className="loader">
            <div>{props.message}</div>
            <div className="loader-spinner">
                <Loader type="ThreeDots" color="#F15451" height="100" width="100" />
            </div>
        </div>
    )
}

export default LoadingIndicator