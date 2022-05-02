import { Link } from 'react-router-dom';
import '../App.css';

function Navigator() {
  return (
    <div className="Navigator">
      <nav>
      <h3>Time series forecasting for passengers</h3>
      <ul className='nvlink'>
        <li><Link to="/">Home</Link></li>
        <li><Link to="/batchProcessing">UploadFile</Link></li>
      </ul>
      </nav>
    </div>
  );
}

export default Navigator;
