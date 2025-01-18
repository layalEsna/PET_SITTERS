
import React, { useEffect, useState } from "react"
import { useParams } from "react-router-dom"
import { useFormik } from 'formik'
import * as Yup from 'yup'

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


    })

    return (
        <div>
            
        </div>
    )
}
export default Appointment