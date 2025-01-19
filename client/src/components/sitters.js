import React, { useEffect, useState } from "react"
import { useNavigate } from 'react-router-dom'
function Sitters() {

    const navigate = useNavigate()

    const [sitters, setSitters] = useState([])

    
    useEffect(() => {
        fetch('http://localhost:5000/sitters')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok')
                }
                return response.json()
            })
            .then((data) => {
                setSitters(data)
            })
            .catch((error) => {
                console.error('Fetch error:', error)
            })
    }, [])



    return (
        <div>
            <h1>Pet Sitters</h1>

            {sitters.map(sitter => (
                <div key={sitter.id}>
                    <button onClick={()=> navigate(`/appointment/${sitter.id}`)}>Book Appointment with: {sitter.name}</button>
                    <p>Address: {sitter.location}</p>
                    <p>Price per day: {sitter.price}</p>
                </div>

            ))}

        </div>
    )



}

export default Sitters