// import custom stylesheet
import "./App.scss"
import axios from "axios";

import Main from "./Main";

axios.defaults.baseURL = "https://o6j35x2u6djfaongyg64jomhmm0wetco.lambda-url.us-west-2.on.aws/";


function App() {
  return (<Main />);
}

export default App;
