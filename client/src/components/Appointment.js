
import React, {useEffect, useState} from "react"
import { useParams } from "react-router-dom"

function Appointment() {
    const { id } = useParams()
    const [sitter, setSitter] = useState('')

    useEffect(() => {
        fetch(`http://localhost:5000/sitters/${id}`)
            .then(res => {
                if (!res.ok) {
                    throw new Error('Failed to fetch sitter.')
                }
                return res.json()
            })
            .then(data =>
                setSitter(data)
            )
            .catch(e => console.error(`Network or server error: ${e}`))
    }, [id])

    return (
        <div>{sitter.name}</div>
    )
}
export default Appointment