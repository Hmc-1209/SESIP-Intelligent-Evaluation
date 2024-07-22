import React, { useContext, useState } from "react";
import { AppContext } from "../App";
import ReactDropdown from "react-dropdown";
import "react-dropdown/style.css"
import CryptoJS from "crypto-js";
import models from './models.json'
// For M1 'brew install pkg-config cairo pango'm then 'npm install @react-pdf-viewer/core@3.12.0'

import "./css/main_app.css";

const MainApp = () => {
    let { alert, setAlert, setMode } = useContext(AppContext);
    const [STFile, setSTFile] = useState(null);
    const [STUrl, setSTUrl] = useState('');
    const model_options = models.available_models;
    const [STInfo, setSTInfo] = useState({ md5: '', sha256: '' });
    const eval_result_status = ['Pending', 'Pass', 'Fail'];
    const [currentEvalResult, setCurrentEvalResult] = useState(eval_result_status[0]);
    const [evalResultPassFailNums, setEvalResultPassFailNums] = useState([0, 0, 0, 0]);
    // Evaluation results should contain 1.name 2.status(pass or fail) 3.detail explain of the result
    const [evalResults, setEvalResults] = useState([
        {"name": "result1", "status": "pass", "detail": "detail 1"},
        {"name": "result2", "status": "fail", "detail": "detail 2"},
        {"name": "result3", "status": "fail", "detail": "detail 3"},
    ]);
    const [selectedResult, setSelectedResult] = useState(null);

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
            setSTFile(file);
            setSTUrl(fileUrl);

            const reader = new FileReader();
            reader.onload = (e) => {
                const binary = e.target.result;
                const md5 = CryptoJS.MD5(CryptoJS.lib.WordArray.create(binary)).toString();
                const sha256 = CryptoJS.SHA256(CryptoJS.lib.WordArray.create(binary)).toString();
                setSTInfo({ md5, sha256 });
            };
            reader.readAsArrayBuffer(file);
        }
    };
    const handleButtonClick = () => {
        document.getElementById('fileInput').click();
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
                <input
                    type="file"
                    id="fileInput"
                    style={{ display: 'none' }}
                    onChange={handleFileChange}
                />
                {STUrl === '' &&
                    <button onClick={handleButtonClick} className="st_upload_btn">
                        Upload Security Target
                    </button>
                }
                <div className="main_app_st_section">
                    {STUrl !== '' && 
                        <div className="st_content_display">
                            <object data={STUrl} type="application/pdf" className="st_content" />
                        </div>
                    }
                    <div className="st_section_right">
                        <div className="st_detail_process">
                            <pre className="st_detail_title">
                                Security Target Details
                            </pre>
                            <pre className="st_detail_information">
                                TOE name : <br /><br />
                                Developer Organization :<br /><br />
                                SESIP Level : 
                            </pre>
                            <pre className="st_detail_title">
                                Checksum
                            </pre>
                            <pre className="st_detail_information">
                                MD5 hash : {STInfo.md5}<br /><br />
                                SHA256 hash : {STInfo.sha256}
                            </pre>    
                        </div>

                        {/* Model select dropdown list */}
                        <div className="model_selector_label">Select Model for evaluation</div>
                        <ReactDropdown options={model_options} value={model_options[0]} className="myControlClassName model_selector"/>
                        
                        {/* Evaluation button and result */}
                        <button className="porocess_evaluation_btn">Evaluate</button>
                        <i><div className={"evaluation_result_label " + 
                                                (currentEvalResult === eval_result_status[0] ? "eval_pending" :
                                                currentEvalResult === eval_result_status[1] ? "eval_pass" :
                                                "eval_fail")
                                        }>
                            {currentEvalResult}
                        </div></i>
                        <pre className="eval_brief_result">
                            {evalResultPassFailNums[0]} SARs passed the evaluation.<br />{evalResultPassFailNums[1]} SARs failed the evaluation.<br /><br />
                            {evalResultPassFailNums[2]} SFRs passed the evaluation.<br />{evalResultPassFailNums[3]} SFRs failed the evaluation.<br />
                        </pre>
                    </div>
                </div>
            </div>
            <div className="main_app_result_section">    
                
                <div className="result_container">
                    {evalResults.map(result => (
                        <button className="result_brief_label" onClick={() => setSelectedResult(result)}>{result.name}</button>
                    ))}
                </div>
                <div className="result_detail_content">
                    {selectedResult ? selectedResult.detail : "Select result for more information."}
                </div>
            </div>
        </div>
    )
};

export default MainApp;