import React, { useContext, useEffect, useState } from "react";
import { ToastContainer, toast } from 'react-toastify';
import { AppContext } from "../App";

import { delete_user, get_user_transfer_token, update_password, update_username } from "../requests/user_requests";

import '@fortawesome/fontawesome-free/css/all.min.css';
import 'react-toastify/dist/ReactToastify.css';
import "./css/setting.css";

const Setting = () => {

    let { setMode, setLoading, setAlert } = useContext(AppContext);
    const [password, setPassword] = useState('');
    const [oldPassword, setOldPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [updateMode, setUpdateMode] = useState(0);
    const [trnasferCode, setTransferCode] = useState(null);

    const error = (error_message) => toast.error(error_message);
    const success = (success_message) => toast.success(success_message);

    // Update the user's username or password
    const submit_update = async () => {
        setLoading(0);
        const access_token = window.localStorage.getItem("access_token");
        if(updateMode === 0) {
            const new_username = document.getElementById("change_username").value;
            if (new_username === "") {
                error("Username cannot be empty.");
                setLoading(false);
                return;
            }

            const response = await update_username(access_token, new_username);
            if (response) {
                if (response === "Data Duplicated.") {
                    error("The username has been registed.");
                    setLoading(false);
                    return;
                }
                success("The username has been updated.")
                setLoading(false);
                return;
            } else {
                error("Unknown error happend. Please Try again later.")
                setLoading(false);
                return;
            }
        } else {
            const old_password = document.getElementById("old_password").value;
            const new_password = document.getElementById("change_password").value;
            const new_password_confirm = document.getElementById("change_password_confirm").value;
            if (old_password === "" || new_password === "" || new_password_confirm === "") {
                error("Information incomplete.");
                setLoading(false);
                return;
            }
            if (new_password !== new_password_confirm) {
                error("Password not match.");
                setLoading(false);
                return;
            }

            const response = await update_password(access_token, old_password, new_password);
            if (response) {
                success("The password has been updated.")
                setLoading(false);
                return;
            } else {
                error("Unknown error happend. Please Try again later.")
                setLoading(false);
                return;
            }
        }
    }

    // Get the transfer token for security target transfer
    const get_transfer_token = async () => {
        const access_token = window.localStorage.getItem("access_token");
        const response = await get_user_transfer_token(access_token);
        if (response) {
            setTransferCode(response);
        }
    }

    const delete_current_user = async () => {
        const access_token = window.localStorage.getItem("access_token");
        const response = await delete_user(access_token);

        if (response) {
            setAlert(3);
            setMode(0);
        }
    }

    // Return to main app page
    const return_main_page = () => {
        setLoading(0);
        setMode(2);
    }

    // Change the settings mode
    useEffect(() => {
        setTransferCode(null);
    }, [updateMode]);

    return (
        <div className="user_setting_panel">
            <pre>User setting panel</pre>
            <div className="updateModeBtnGroup">
                <button className={"updateModeBtn " + (updateMode === 0 ? "light" : "")} onClick={()=>setUpdateMode(0)}><i class="fa-solid fa-gear"></i></button>
                <button className={"updateModeBtn " + (updateMode === 1 ? "light" : "")} onClick={()=>setUpdateMode(1)}><i class="fa-solid fa-lock"></i></button>
                <button className={"updateModeBtn " + (updateMode === 2 ? "light" : "")} onClick={()=>setUpdateMode(2)}><i class="fa-solid fa-exchange"></i></button>
                <button className={"updateModeBtn " + (updateMode === 3 ? "light" : "")} onClick={()=>setUpdateMode(3)}><i class="fa-solid fa-trash"></i></button>
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
                    <button className="setting_submit_btn" onClick={submit_update}>Submit</button>
                </div>
            ) : updateMode === 1 ? (
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
                        autoComplete=""
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
                        autoComplete=""
                    />
                    <button className="setting_submit_btn" onClick={submit_update}>Submit</button>
                </div>
            ) : updateMode === 2 ? (
                <div className="updateInputContainer">
                    
                    {trnasferCode === null ? 
                        <button className="generate_transfer_code" onClick={get_transfer_token}>Generate transfer code</button> :
                        <>
                            <div className="generated_transfer_code">
                                Copy and paste it on the Security Target transfer code section :
                            </div>
                            <b className="transfer_code">{trnasferCode}</b>
                        </>
                    }
                </div>
            ) : (
                <div className="updateInputContainer">
                    <b className="delete_user_warning">Warning: This action cannot be trace back.</b>
                    <b className="delete_user_warning">The user will be deleted forever!</b>

                    <button className="delete_user" onClick={delete_current_user}><b>Delete User</b></button>
                </div>
            )}
            
            
            <i className="fa-solid fa-rotate-left return_btn" onClick={return_main_page}></i>
            <ToastContainer theme="colored" className="alert" limit={1} autoClose={2000}/>
        </div>
    )
};

export default Setting;