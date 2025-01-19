import { useNavigate } from 'react-router-dom'
function NavBar() {
    const navigate = useNavigate()
    return (
        <nav>
            <button onClick={()=> navigate('/sitters')}>Pet Sitters</button>
            {/* <button onClick={()=> navigate('/appointment')}>Appointment</button> */}
           
       </nav>
   ) 
}
export default NavBar