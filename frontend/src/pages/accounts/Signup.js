import React, { useState } from "react";
import Axios from "axios";
import {
    Form,
    Input,
    Button,
    Select,
    notification,
  } from 'antd';
  import { SmileOutlined, FrownOutlined } from "@ant-design/icons"
  import 'antd/dist/antd.css';
import "./scss/signup.scss"

const Signup = () => {

    const [fieldErrors, setFieldErrors] = useState({});

    const onFinish = (values) => {

        async function fn(){

            const { username, email, password, password1, gender } = values;

            setFieldErrors({})
            const data = {username, email, password, gender}
            console.log("data : ", data)

            if (password != password1){
                notification.open({
                    message:"비밀번호 오류",
                    description:"비밀번호가 일치하지 않습니다.",
                    placement:"topLeft",
                    icon: <FrownOutlined style={{color:"#ff3333"}} />,
                });
            }else{
                try {
                    await Axios.post("http://127.0.0.1:8000/accounts/signup/", data)
                    notification.open({
                        message:"회원가입 성공",
                        description:"로그인 페이지로 이동합니다.",
                        placement:"topLeft",
                        icon: <SmileOutlined style={{color:"#108ee9"}} />,
                    });
                } catch (error) {
    
                    setFieldErrors({
                        "signupError": "이미 존재하는 사용자입니다."
                    });
    
                    notification.open({
                        message:"회원가입 실패",
                        description: fieldErrors["signupError"],
                        placement:"topLeft",
                        icon: <FrownOutlined style={{color:"#ff3333"}}/>,
                    });
                }
            }
        }
        fn();
    }


    return(
        <div className="signup">
            <h3 className="signup__title">회원가입</h3>
            <div className="signup__form">
                <Form
                layout="horizontal"
                onFinish={onFinish}
                >
                    <Form.Item label="닉네임" name="username" rules={[{required:true, message:"닉네임을 입력해주세요."}]} hasFeedback>
                        <Input />
                    </Form.Item>

                    <Form.Item label="이메일" name="email" rules={[{required:true, message:"이메일을 입력해주세요.", type:"email"}]} hasFeedback>
                        <Input />
                    </Form.Item>

                    <Form.Item label="비밀번호" name="password" rules={[{required:true, message:"비밀번호를 입력해주세요."}]} hasFeedback>
                        <Input.Password/>
                    </Form.Item>

                    <Form.Item label="비밀번호 확인" name="password1" rules={[{required:true, message:"비밀번호를 입력해주세요."}]} hasFeedback>
                        <Input.Password/>
                    </Form.Item>

                    <Form.Item label="성별" name="gender" hasFeedback>
                        <Select>
                            <Select.Option value="남자">남자</Select.Option>
                            <Select.Option value="여자">여자</Select.Option>
                        </Select>
                    </Form.Item>

                    <Form.Item>
                        <Button type="primary" htmlType="submit">회원가입</Button>
                    </Form.Item>
                </Form>
            </div>
          </div>
    );
}

export default Signup;