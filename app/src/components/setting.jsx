import React, { useContext, useState } from "react";

import { AppContext } from "../App";
import { ToastContainer, toast } from 'react-toastify';
import '@fortawesome/fontawesome-free/css/all.min.css';
import 'react-toastify/dist/ReactToastify.css';

import "./css/setting.css";

const Setting = () => {

    let { setMode, setLoading } = useContext(AppContext);
    const [password, setPassword] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [updateMode, setUpdateMode] = useState(0);

    const submit_update = () => {
        setLoading(0);
    }

    const return_main_page = () => {
        setLoading(0);
        setMode(2);
    }

    return (
        <div className="user_setting_panel">
            <pre>User setting panel</pre>
            <div className="updateModeBtnGroup">
                <button className={"updateModeBtn " + (updateMode === 0 ? "light" : "")} onClick={()=>setUpdateMode(0)}><i class="fa-solid fa-gear"></i></button>
                <button className={"updateModeBtn " + (updateMode === 1 ? "light" : "")} onClick={()=>setUpdateMode(1)}><i class="fa-solid fa-lock"></i></button>
            </div>
            {updateMode === 0 ? (
                <div className="updateInputContainer">
                    <label htmlFor="change_username" className="setting_input_label">
                        New username:
                    </label>
                    <input
                        type="text"
                        name="change_username"
                        id="change_username"
                        className="setting_input"
                        placeholder="Leave empty if no update needed."
                    />
                </div>
            ) : (
                <div className="updateInputContainer">
                    <label htmlFor="old_password" className="setting_input_label">
                        Old password:
                    </label>
                    <input
                        type="password"
                        name="old_password"
                        id="old_password"
                        className="setting_input"
                        placeholder="Enter old password to change."
                        value={oldPassword}
                        onChange={(e) => setOldPassword(e.target.value)}
                    />
                    <label htmlFor="change_password" className={`setting_input_label ${password === '' ? 'grey' : ''}`}>
                        New password:
                    </label>
                    <input
                        type="password"
                        name="change_password"
                        id="change_password"
                        className={`setting_input ${oldPassword === '' ? 'disabled grey' : ''}`}
                        placeholder="Enter the new password."
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        disabled={oldPassword === ''}
                    />
                    <label htmlFor="change_password_confirm" className={`setting_input_label ${password === '' ? 'grey' : ''}`}>
                        Confirm new password:
                    </label>
                    <input
                        type="password"
                        name="change_password_confirm"
                        id="change_password_confirm"
                        className={`setting_input ${oldPassword === '' ? 'disabled grey' : ''}`}
                        placeholder="Enter the same password."
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        disabled={oldPassword === ''}
                    />
                </div>
            )}
            
            
            <i className="fa-solid fa-rotate-left return_btn" onClick={return_main_page}></i>
            <button className="setting_submit_btn">Submit</button>
        </div>
    )
};

export default Setting;