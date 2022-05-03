import "react-dates/initialize"; 
import { DateRangePicker } from "react-dates"; 
import "react-dates/lib/css/_datepicker.css";
import '../App.css';
import { useState } from "react";
import Chart from "./Chart";

function Home() {
  return (
    <div className="Home">
      <JsonForm></JsonForm>
    </div>
  );
}

export default Home;

const JsonForm = ()=> {

  const [startDate, setStartDate] = useState(null)
  const [endDate, setEndDate] = useState(null)
  const [focusedInput, setFocusedInput] = useState()
  const [startDateFormatted, setStartDateFormatted] = useState(null)
  const [endDateFormatted, setEndDateFormatted] = useState(null)
  const [data, setData] = useState([])
  
  const hundleDateChange = (startDate, endDate) => { 
    setStartDate(startDate)
    setEndDate(endDate)

    if (startDate != null) {
      setStartDateFormatted(startDate.format("D-MM-Y"))
     } 
    if (endDate != null) { 
      setEndDateFormatted(endDate.format("D-MM-Y"))
     } 
    }

    const handleSubmit = async (event) => {
      event.preventDefault()
      const url = new URL("http://localhost:8000/predict_from_dates")
      var params = {'startDate':startDate, 'endDate': endDate}
      url.search = new URLSearchParams(params).toString()
      const reqOpt = {method: "POST",  headers: {"Content-type": "application/json"},  body: JSON.stringify()}
      const resp = await fetch(url,reqOpt)
        .then((response) => (response.json()))
        .then(data => {
          setData(data)
          return data})
        .catch(error => {console.log(error)})

      console.log(resp)
    }
  
  return(
    <>
    <DateRangePicker 
    startDate={startDate} 
    startDateId="start_date_id" 
    endDate={endDate} 
    endDateId="end_date_id" 
    onDatesChange={({ startDate, endDate }) => hundleDateChange(startDate, endDate) } 
    focusedInput={focusedInput} 
    onFocusChange={(focusedInput) => setFocusedInput(focusedInput)} /> 
    <form onSubmit={handleSubmit}>
      <input type="submit" value="submit"></input>
    </form>
    <Chart data={data}></Chart>
    </>
    
  )
}