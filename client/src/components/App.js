import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import Sitters from './Sitters'
import SignupForm from "./SignupForm"
import LoginForm from "./Login"
import Appointment from "./Appointment";

function App() {
  return (
    <Router>
      <div>
        <h1>Project Client</h1>;
        <Routes>
          <Route path='/sitters' element={<Sitters />} />
          <Route path='/signup' element={<SignupForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/sitters/:id" element={<Appointment />} />
        </Routes>
      </div>
    </Router>)
}

export default App;
