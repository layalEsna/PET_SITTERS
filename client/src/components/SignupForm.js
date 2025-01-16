
import React, { useState } from 'react';
import { useFormik } from 'formik';
import { useNavigate } from 'react-router-dom'
import * as Yup from 'yup';

function SignupForm() {
    // const { confirm_password, ...signupData } = values
    const navigate = useNavigate()
    const [errorMessage, setErrorMessage] = useState('')
    
    const passwordPattern = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[!@#$%^&*]).{8,}$/

    const formik = useFormik({
        initialValues: {
            user_name: '',
            password: '',
            confirm_password: ''
        },
        validationSchema: Yup.object({
            user_name: Yup.string()
                .required('Username is required.')
                .min(5, 'Username must be at least 5 characters long.'),
            password: Yup.string()
                .required('Password is required.')
                .min(8, 'Password must be at least 8 characters long.')
                .matches(passwordPattern, 'Password must be at least 8 characters long and include at least 1 lowercase letter, 1 uppercase letter, and 1 special character (!@#$%^&*).'),
            confirm_password: Yup.string()
                .oneOf([Yup.ref('password'), null], 'Password must match.')
                .required('Confirm password is required.')

        }),

        onSubmit: (values) => {

            console.log('Submitting form values:', values);


            fetch('http://localhost:5000/signup', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(values),
            })
                .then((res) => {
                    if (!res.ok) {
                        throw new Error('Failed to signup.');
                    }
                    return res.json();
                })
                .then((data) => {
                    console.log('Server response:', data); // Log server response
                    navigate('/sitters')
                    
                })
                .catch((e) => {
                    setErrorMessage(e.message);
                    console.error('Network or server error:', e);
                });                        
        }
    })
}
export default SignupForm