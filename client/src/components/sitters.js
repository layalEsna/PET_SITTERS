import React, { useEffect, useState } from "react"

function Sitters() {

    const [sitters, setSitters] = useState([])

    //     useEffect(() => {
    //         console.log("Fetching sitters...")
    //         fetch('http://localhost:3001/sitters')
    //             .then(res => {
    //                 if (!res.ok) {
    //                 throw new Error('Failed to fetch sitters.')
    //                 }
    //                 return res.json()
    //         })
    //         .then((data) => {
    //             setSitters(data); // Assuming you're storing the sitters data in state
    //         })
    //         .catch((error) => {
    //             console.error('Fetch error:', error);
    //         });
    // }, []);
    useEffect(() => {
        fetch('http://localhost:5000/sitters')
            .then((response) => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then((data) => {
                setSitters(data); // Assuming you're storing the sitters data in state
            })
            .catch((error) => {
                console.error('Fetch error:', error);
            });
    }, []);



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