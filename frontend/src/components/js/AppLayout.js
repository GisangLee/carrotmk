import React from "react";
import AppHeader from "./AppHeader"
import AppFooter from "./AppFooter"
import { Button } from 'antd';


const AppLayout = ({children}) => {
    return(
        <>
            <AppHeader/>
            {children}
            <Button type="primary" href="upload/">포스팅</Button>
            <AppFooter/>
        </>
    )
}

export default AppLayout;