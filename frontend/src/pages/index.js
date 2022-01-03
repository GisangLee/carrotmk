import React from "react";
import { Route, Routes } from "react-router-dom";
import AppLayout from "../components/js/AppLayout";
import Signup from "./accounts/Signup";
import Login from "./accounts/Login";
import Home from "./Home";
import LoginRequiredRoute from "../utils/LoginRequiredRoute";

const Root = () => {
    return (
        <AppLayout>
            <Routes>
                <Route
                    path="/profile"
                    element={
                        <LoginRequiredRoute>
                            <Home/>
                        </LoginRequiredRoute>
                    }
                />
                <Route path="signup/" element={<Signup/>}/>
                <Route path="login/" element={<Login/>}/>
            </Routes>
        </AppLayout>
    );
}



export default Root;