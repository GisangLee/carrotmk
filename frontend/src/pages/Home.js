import React from 'react'
import { Button } from "antd";
import 'antd/dist/antd.css';
import axios from 'axios';


const Home = () => {

    const logout = async () => {
        const jwtToken = JSON.parse(localStorage.getItem("jwtToken"));
        const headers = {Authorization: `JWT ${jwtToken}`};
        const response = await axios.get("http://127.0.0.1:8000/accounts/logout/", {headers});
        
        console.log("response : ", response);
        window.localStorage.removeItem("jwtToken");
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