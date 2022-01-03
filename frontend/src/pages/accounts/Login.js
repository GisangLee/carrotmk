import React from 'react'
import { Form, Input, Button } from 'antd';
import 'antd/dist/antd.css';
import "./scss/login.scss";

const Login = () => {
    return(
        <div className="login">
            <h3 className='login__title'>로그인</h3>
            <div className='login__form'>
                <Form
                    name="basic"
                    labelCol={{ span: 8 }}
                    wrapperCol={{ span: 16 }}
                    autoComplete="off"
                >
                    <Form.Item
                        label="이메일"
                        name="email"
                        rules={
                            [
                                {
                                    required: true,
                                    message: '이메일을 입력해 주세요.',
                                    type:"email",
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