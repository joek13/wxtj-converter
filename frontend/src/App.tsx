// import custom stylesheet
import "./App.scss"
import axios from "axios";

import Main from "./Main";

axios.defaults.baseURL = "https://mlnaw218id.execute-api.us-east-1.amazonaws.com";

function App() {
  return (<Main />);
}

export default App;
