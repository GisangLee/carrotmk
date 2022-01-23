import React from "react";
import AppHeader from "./AppHeader"
import AppFooter from "./AppFooter"
import { Button } from 'antd';


const AppLayout = ({children}) => {
    const jwtToken = localStorage.getItem("jwtToken");
    return(
        <>
            <AppHeader/>
            {children}
            <Button type="primary" href="/upload">포스팅</Button>
            {jwtToken === null ? (
                <Button type="primary" href="/login">로그인</Button>
            ) : (
                null
            )}
            <Button type="primary" href="/profile">프로필</Button>
            <AppFooter/>
        </>
    )
}

export default AppLayout;