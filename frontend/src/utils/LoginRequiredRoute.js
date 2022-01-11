import React from 'react'
import { Route, Navigate, useLocation } from 'react-router-dom';
import Login from '../pages/accounts/Login';

const LoginRequiredRoute = ({children}) => {
    const isAuthenticated = window.localStorage.getItem("isAuthenticated");

    console.log("isAuthenticated", isAuthenticated==="false");
    console.log("isAuthenticated", typeof(isAuthenticated));

    return !isAuthenticated ? (
        <Navigate to="/login"/>
    ) : (
        children
    )

};

export default LoginRequiredRoute;