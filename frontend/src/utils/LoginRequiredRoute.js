import React from 'react'
import { Route, Navigate, useLocation } from 'react-router-dom';
import Login from '../pages/accounts/Login';

const LoginRequiredRoute = ({children}) => {
    const isAuthenticated = window.localStorage.getItem("isAuthenticated");

    return !isAuthenticated ? (
        <Navigate to="/login"/>
    ) : (
        children
    )

};

export default LoginRequiredRoute;