import React from "react";
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'; // Import BrowserRouter

import Sitters from './Sitters'
import SignupForm from "./SignupForm"
import LoginForm from "./Login"
import Appointment from "./Appointment"
// import NavBar from "./NavBar"

function App() {
  return (
    <Router>
      <header>

        {/* <NavBar /> */}
        
      </header>
      <main>
        <Routes>
          <Route path='/sitters' element={<Sitters />} />
          <Route path='/signup' element={<SignupForm />} />
          <Route path="/login" element={<LoginForm />} />
          <Route path="/appointment/:id" element={<Appointment />} />
        </Routes>
      </main>
    </Router>)
}

export default App;
