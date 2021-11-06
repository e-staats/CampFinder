import React from 'react';
import Helmet from 'react-helmet';
import DayPicker from 'react-day-picker';

class DateRangePicker extends React.Component {
  static defaultProps = {
    numberOfMonths: 2,
  };

  handleDayClick = day => {
    this.props.handleDayClick(day)
  }

  handleResetClick = () => {
    this.props.handleResetClick()
  }

  render() {
    const from = this.props.from
    const to = this.props.to;
    const modifiers = { start: from, end: to };
    return (
      <div className="formDayPicker">
        <p>
          {!from && !to && 'Please select the first day.'}
          {from && !to && 'Please select the last day.'}
          {from &&
            to &&
            `Selected from ${from.toLocaleDateString()} to
                ${to.toLocaleDateString()}`}{' '}
          {from && to && (
            <a className="resetLink" tabIndex={0} onClick={this.handleResetClick}>
              (Reset)
            </a>
          )}
        </p>
        <DayPicker
          className="Selectable"
          numberOfMonths={this.props.numberOfMonths}
          selectedDays={[from, { from, to }]}
          modifiers={modifiers}
          onDayClick={this.handleDayClick}
        />
        <Helmet>
          <style>{`
  .Selectable .DayPicker-Day--selected:not(.DayPicker-Day--start):not(.DayPicker-Day--end):not(.DayPicker-Day--outside) {
    background-color: #ea9285 !important;
    color: #FFFFFF;
  }
  .Selectable .DayPicker-Day {
    border-radius: 0 !important;
  }
  .Selectable .DayPicker-Day--start {
    border-top-left-radius: 50% !important;
    border-bottom-left-radius: 50% !important;
  }
  .Selectable .DayPicker-Day--end {
    border-top-right-radius: 50% !important;
    border-bottom-right-radius: 50% !important;
  }
`}</style>
        </Helmet>
      </div>
    );
  }
}


export default DateRangePicker;