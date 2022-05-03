import { useState } from 'react';
import '../App.css';
import Chart from './Chart';

function UploadFile() {

  const [data,setData] = useState([])
  const [selectFile, setSelectFile] = useState("")
  let dataAux = []

  const handleSubmit = (event)=> {
    console.log(event.target.name,event.target.files[0])
    setSelectFile(event.target.files[0])
  }

  const handleUpload = async (event) => {
    event.preventDefault()
    const url = "http://localhost:8000/predict_from_file"
    const formData = new FormData()
    formData.append('file', selectFile, selectFile.name)

    const reqOpt = {method:"POST", body:formData}
    const resp = await fetch(url, reqOpt)
    .then(resp => resp.json())
    .then(resp2 => {
      resp2.forEach(e => {
        dataAux.push({'date': '01/'.concat(e.MonthNum, '/', e.Year), 'value':e.Label })
    });
    setData(dataAux)
    })

    console.log(data)

    
    setData(dataAux)
  }

  return (
    <div className="UploadFile">
      <form onSubmit={handleUpload}>
        <input type="file" name="selectFile" onChange={handleSubmit}></input>
        <input type="submit" value="submit"></input>
      </form>
      <Chart data={data}></Chart>
      
    </div>
  );
}

export default UploadFile;
