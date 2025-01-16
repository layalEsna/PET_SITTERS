import React, {useEffect, useState} from "react"

function Sitters() {

    const [sitters, setSitters] = useState([])

    useEffect(() => {
        fetch('sitters')
            .then(res => {
                if (!res.ok) {
                throw new Error('Failed to fetch sitters.')
                }
                return res.json()
        })
        .then(data=> setSitters(data))
        .catch(e=> console.error(e))
    }, [])

    return (
        <div>
            <h1>Pet Sitters</h1>
            
            {sitters.map(sitter => (
                <div key={sitter.id}>
                <button>Book Appointment with: {sitter.name}</button>
                    <p>Address: {sitter.location}</p>
                    <p>Price per day: {sitter.price}</p>
                    </div>

            ))}

        </div>
    )


    
}

export default Sitters