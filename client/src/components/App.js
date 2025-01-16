import React from "react";
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom'; // Import BrowserRouter

import Sitters from './Sitters'

function App() {
  return(
  <Router>
    <div>
      <h1>Project Client</h1>;
      <Switch>
        <Route path='/sitters' component={Sitters} />
      </Switch>
    </div>
  </Router>)
}

export default App;
