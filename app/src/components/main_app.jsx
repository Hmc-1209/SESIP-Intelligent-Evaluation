import React, { useContext, useState } from "react";
import { AppContext } from "../App";
import { Viewer, Worker } from '@react-pdf-viewer/core';
import '@react-pdf-viewer/core/lib/styles/index.css';
// For M1 'brew install pkg-config cairo pango'm then 'npm install @react-pdf-viewer/core@3.12.0'

import "./css/main_app.css";

const MainApp = () => {
    let { alert, setAlert, setMode } = useContext(AppContext);
    const [pdfFile, setPdfFile] = useState(null);
    const [pdfUrl, setPdfUrl] = useState('');

    const logOut = () => {
        window.localStorage.setItem("access_token", null);
        window.localStorage.setItem("username", null);
        window.localStorage.setItem("user_id", null);
        setAlert(1);
        setMode(0);
    }

    const handleFileChange = (event) => {
        const file = event.target.files[0];
        if (file) {
          const fileUrl = URL.createObjectURL(file);
          console.log(fileUrl)
          setPdfFile(file);
          setPdfUrl(fileUrl);
        }
      };

    
    return (
        <div className="main_app_page">

            {/* Navbar */}
            <div className="main_app_navbar">
                <div>
                    SESIP Intelligence Eval
                    <div className="main_app_navbar_subtitle">LLM evaluated result will be provided using this tool.</div>
                </div>
                <div className="main_app_navbar_button_group">
                    <button className="main_app_navbar_button" onClick={logOut}>Log out</button>
                </div>
            </div>

            {/* Evaluation section */}
            <div className="main_app_content_section">
                {!pdfUrl && 
                <input
                    type="file"
                    id="fileInput"
                    accept="application/pdf"
                    onChange={handleFileChange}
                />}
                {pdfUrl && 
                <div style={{ height: '800px', width: '100%' }}>
                    <Worker workerUrl="https://unpkg.com/pdfjs-dist@3.12.0/build/pdf.worker.min.js">
                        <Viewer fileUrl={pdfUrl} />
                    </Worker>
                </div>}
            </div>
        </div>
    )
};

export default MainApp;