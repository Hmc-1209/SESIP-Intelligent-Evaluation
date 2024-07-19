import React, { useContext } from "react";
import { AppContext } from "../App";


import "./css/main_app.css";


const MainApp = () => {
    let { alert, setAlert, setMode } = useContext(AppContext);

    const logOut = () => {
        window.localStorage.setItem("access_token", null);
        window.localStorage.setItem("username", null);
        window.localStorage.setItem("user_id", null);
        setAlert(1);
        setMode(0);
    }

    
    return (
        <div className="main_app_page">
            <div className="main_app_navbar">
                <div>
                    SESIP Intelligence Eval
                    <div className="main_app_navbar_subtitle">LLM evaluated result will be provided using this tool.</div>
                </div>
                <div className="main_app_navbar_button_group">
                    <button className="main_app_navbar_button" onClick={logOut}>Log out</button>
                </div>
            </div>
            <div className="main_app_content_section">123</div>
        </div>
    )
};

export default MainApp;