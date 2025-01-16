import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import Sitters from './Sitters'
import SignupForm from "./SignupForm";

function App() {
  return (
    <Router>
      <div>
        <h1>Project Client</h1>;
        <Routes>
          <Route path='/sitters' element={<Sitters />} />
          <Route path='/signup' element={<SignupForm/> } />
        </Routes>
      </div>
    </Router>)
}

export default App;
