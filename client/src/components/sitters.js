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


    
}

export default Sitters