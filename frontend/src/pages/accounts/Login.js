import React, { useState }from 'react'
import { useNavigate } from 'react-router-dom';
import Axios from 'axios';
import { Form, Input, Button, notification } from 'antd';
import { SmileOutlined, FrownOutlined } from "@ant-design/icons";
import 'antd/dist/antd.css';
import "./scss/login.scss";
import useLocalStorage from '../../utils/useLocalStorage';

const Login = () => {

    const [fieldErrors, setFieldErrors] = useState({});

    const navigate = useNavigate();

    const [jwtToken, setJwtToken] = useLocalStorage("jwtToken", "");
    const [isAuthenticated, setIsAuthenticated] = useLocalStorage("isAuthenticated", false);

    const onFinish = (values) => {
        async function fn(){
            const { username, password } = values;

            setFieldErrors({});

            const data = { username, password };
            console.log("data", data);
            
            try {
                const response = await Axios.post("http://127.0.0.1:8000/accounts/token/auth/", data)

                const { data : { token: jwtToken }} = response;

                if (jwtToken === undefined){
                    notification.open({
                        message:"로그인 실패",
                        description:"정보를 정확히 입력해 주세요",
                        placement:"topLeft",
                        icon:<FrownOutlined style={{color:"#ff3333"}}/>
                    });
                    navigate("/login");
                }else{
                    notification.open({
                        message:"로그인 성공",
                        description:"메인 페이지로 이동합니다.",
                        placement:"topLeft",
                        icon:<SmileOutlined style={{color:"#108ee9"}}/>
                    });
                    setJwtToken(jwtToken);
                    setIsAuthenticated(true);
                    navigate("/");
                }




            } catch (error) {
                setFieldErrors({
                    "loginError": "정보를 정확하게 입력하세요."
                })
                notification.open({
                    message:"로그인 실패",
                    description:fieldErrors["loginError"],
                    placement:"topLeft",
                    icon:<FrownOutlined style={{color:"#ff3333"}} />
                });
            }
        }
        fn();
    }

    return(
        <div className="login">
            <h3 className='login__title'>로그인</h3>
            <div className='login__form'>
                <Form
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    autoComplete="off"
                    onFinish={onFinish}
                >
                    <Form.Item
                        label="닉네임"
                        name="username"
                        rules={
                            [
                                {
                                    required: true,
                                    message: '닉네임을 입력해주세요.',
                                }
                            ]
                        }
                    >
                        <Input />
                    </Form.Item>

                    <Form.Item
                        label="비밀번호"
                        name="password"
                        rules={
                            [
                                {
                                    required: true,
                                    message: '비밀번호를 입력해 주세요.'
                                }
                            ]
                        }
                    >
                        <Input.Password />
                    </Form.Item>

                    <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                        <Button type="primary" htmlType="submit">로그인</Button>
                    </Form.Item>
            </Form>
            </div>
        </div>
    )
}

export default Login;