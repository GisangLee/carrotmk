import React from 'react'
import { Link, Route, Navigate, useLocation } from 'react-router-dom';
import Login from '../pages/accounts/Login';

const LoginRequiredRoute = ({children}) => {
    const isAuthenticated = window.localStorage.getItem("isAuthenticated");

    return !isAuthenticated ? (
        <Link to="login/"/>
    ) : (
        children
    )

};

export default LoginRequiredRoute;