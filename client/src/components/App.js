import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import Sitters from './Sitters'

function App() {
  return (
    <Router>
      <div>
        <h1>Project Client</h1>;
        <Routes>
          <Route path='/sitters' element={<Sitters />} />
        </Routes>
      </div>
    </Router>)
}

export default App;
