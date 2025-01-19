
import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useFormik } from 'formik'
import * as Yup from 'yup'
import NavBar from "./NavBar"

function Appointment() {
    const { id } = useParams()
    const [sitter, setSitter] = useState({})
    const [confirmationMessage, setConfirmationMessages] = useState(() => {
        const storeMessages = localStorage.getItem('confirmationMessage')
        return storeMessages ? JSON.parse(storeMessages) : []

    })

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

    useEffect(() => {
        localStorage.setItem('confirmationMessage', JSON.stringify(confirmationMessage));
    }, [confirmationMessage])

    const formik = useFormik({
        initialValues: {
            pet_name: '',
            pet_type: '',
            date: '',
            duration: ''
        },
        validationSchema: Yup.object({
            pet_name: Yup.string()
                .required('Pet name is required.'),
            pet_type: Yup.string()
                .required('Pet type is required.'),
            date: Yup.date()
                .required('Date is required.')
                .min(new Date(), 'Date and time must be in the future.'),
            duration: Yup.number()
                .required('Duration is required.')
                .min(1, 'Duration must be between 1 and 10 inclusive.')
                .max(10, 'Duration must be between 1 and 10 inclusive.')



        }),
        onSubmit: (values) => {
            fetch('http://127.0.0.1:5000/appointment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(values)
            })
                .then(res => {
                    if (!res.ok) {
                    throw new Error('Failed to submit.')
                    }
                    return res.json()
            })
            .then(() => {
                const newMessage = `Appointment with: ${sitter.name} booked for ${values.pet_name}, Date: ${values.date}, Duration: ${values.duration} days, total price: $${sitter.price * values.duration}`;
                setConfirmationMessages((prevMessages) => [...prevMessages, newMessage]); // Append to array
            })
            .catch(e => console.error(e))
    }
})

    return (
        <div>
            <div>
                <NavBar />
            </div>
            <br/>
            <form onSubmit={formik.handleSubmit}>

                <div>
                    <label htmlFor="pet_name">Pet Name</label>
                    <input
                        id="pet_name"
                        type="text"
                        name="pet_name"
                        value={formik.values.pet_name}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}

                    />
                    {formik.errors.pet_name && formik.touched.pet_name && (
                        <div className="error">{formik.errors.pet_name}</div>
                    )}
                </div>
                <br/>
                <div>
                    <label htmlFor="pet_type">Pet Type</label>
                    <select
                        id="pet_type"
                        value={formik.values.pet_type}
                        onChange={formik.handleChange}
                        onBlur={formik.handleBlur}
                    >
                        <option value=''>select one</option>
                        <option value='cat'>cat</option>
                        <option value='dog'>dog</option>
                        <option value='bird'>bird</option>
                    </select>
                    {formik.errors.pet_type && formik.touched.pet_type && (
                        <div className="error">{formik.errors.pet_type}</div>
                    )}
                </div>
                <br/>
                <div>
                    <label htmlFor="date">Date</label>
                    <input
                        id="date"
                        type="date"
                        name="date"
                        value={formik.values.date}
                        onBlur={formik.handleBlur}
                        onChange={formik.handleChange}

                    />
                    {formik.errors.date && formik.touched.date && (
                        <div className="error">{formik.errors.date}</div>
                    )}
                </div>
                <br/>
                <div>
                    <label htmlFor="duration">Duration</label>
                    <select
                        id="duration"
                        name="duration"
                        value={formik.values.duration}
                        onChange={e => formik.setFieldValue('duration', parseInt(e.target.value))}
                        onBlur={formik.handleBlur}
                    >
                        <option value=''>select one</option>
                        <option value='1'>1 day</option>
                        <option value='2'>2 days</option>
                        <option value='3'>3 days</option>
                        <option value='4'>4 days</option>
                        <option value='5'>5 days</option>
                        <option value='6'>6 days</option>
                        <option value='7'>7 days</option>
                        <option value='8'>8 days</option>
                        <option value='9'>9 days</option>
                        <option value='10'>10 days</option>
                    </select>
                    {formik.errors.duration && formik.touched.duration && (
                        <div className="error">{formik.errors.duration}</div>
                    )}
                </div>
                <br />
                <div>
                    <button type="submit">submit</button>
                </div>

                

            </form>
            <div>
                <h2>Your Appointments:</h2>
                <ul>
                    {confirmationMessage.map((message, index)=>(
                        <li key={index}>{message}</li>
                    ))}
                </ul>
            </div>
            

        </div>
    )
}
export default Appointment