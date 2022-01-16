import React, { useState } from 'react';
import { Form, Input, Button, Upload } from 'antd';
import { UploadOutlined } from "@ant-design/icons";
import axios from 'axios';
import { useNavigate } from "react-router-dom";

const PostUpload = () => {
    const [fileList, setFileList] = useState([]);
    let navigate = useNavigate();

    const jwtToken = localStorage.getItem("jwtToken");

    const handleOnChangeUpload = ({fileList}) => {
        setFileList(fileList);
    }

    const handleOnFinish = async (fieldValues) => {
        console.log("fieldValues", fieldValues);
        const formData = new FormData()

        const {title, desc, photos:{fileList}} = fieldValues;

        formData.append("title", title);
        formData.append("desc", desc);
        

        fileList.forEach(file => {
            formData.append("photos", file.originFileObj);
        });
        const headers = {Authorization: `JWT ${jwtToken}`};
        console.log("headers :", headers);
        try {
            const response = await axios.post("http://127.0.0.1:8000/posts/post/upload", formData, {headers});
            console.log("SUCCESS ", response);
            navigate('/');
        } catch (error) {
            console.log("error", error);
        }
    }

    return(
        <Form name="postupload" onFinish={handleOnFinish}>
            <Form.Item
                name="title"
                label="title"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 5 }}
            >
                <Input/>
            </Form.Item>
            <Form.Item
                name="desc"
                label="desc"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 5 }}
            >
                <Input.TextArea/>
            </Form.Item>
            <Form.Item
                name="photos"
                label="photos"
                labelCol={{ span: 8 }}
                wrapperCol={{ span: 16 }}
            >
                <Upload name="photo" action="/upload.do" listType="picture" fileList={fileList} onChange={handleOnChangeUpload} beforeUpload={() => false}>
                <Button icon={<UploadOutlined />}>Click to upload</Button>
                </Upload>
            </Form.Item>
            {JSON.stringify(fileList)}
            <Form.Item wrapperCol={{ offset: 8, span: 16 }}>
                <Button type="primary" htmlType="submit">Submit</Button>
            </Form.Item>
            
        </Form>
    );
}

export default PostUpload;