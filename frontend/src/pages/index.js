import React from "react";
import { Route, Routes } from "react-router-dom";
import AppLayout from "../components/js/AppLayout";
import Signup from "./accounts/Signup";

const Root = () => {
    return (
        <AppLayout>
            <Routes>
                <Route path="/" element={<Signup/>}/>
            </Routes>
        </AppLayout>
    );
}



export default Root;