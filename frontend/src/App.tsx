// import custom stylesheet
import "./App.scss"
import axios from "axios";

import Main from "./Main";

if (!process.env.NODE_ENV || process.env.NODE_ENV === 'development') {
  axios.defaults.baseURL = "https://mlnaw218id.execute-api.us-east-1.amazonaws.com";
} else {
  axios.defaults.baseURL = "https://k3eycnkg18.execute-api.us-east-1.amazonaws.com/";
}


function App() {
  return (<Main />);
}

export default App;
