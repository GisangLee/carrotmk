import React from 'react'
import { Button } from "antd";
import 'antd/dist/antd.css';


const Home = () => {

    const logout = () => {
        window.localStorage.removeItem("jwtToken")
        window.localStorage.removeItem("isAuthenticated");
    };

    return(
        <div>
            홈
            <Button type='primary' onClick={logout}>로그아웃</Button>
        </div>
    );
}

export default Home;