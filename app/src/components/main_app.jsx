import React, { useContext, useEffect, useState } from "react";
import { AppContext } from "../App";
import ReactDropdown from "react-dropdown";
import "react-dropdown/style.css";
import CryptoJS from "crypto-js";
import models from './models.json';
import '@fortawesome/fontawesome-free/css/all.min.css';
import get_user_st from "../requests/user_requests";
// For M1 'brew install pkg-config cairo pango'm then 'npm install @react-pdf-viewer/core@3.12.0'

import "./css/main_app.css";

const MainApp = () => {

    // Static variables
    const model_options = models.available_models;
    const eval_result_status = ['Pending', 'Pass', 'Fail'];
    
    // Context variables
    let { alert, setAlert, setMode, setLoading } = useContext(AppContext);

    // useState variables
    const [userST, setUserST] = useState(null);
    const [STFile, setSTFile] = useState(null);
    const [STUrl, setSTUrl] = useState('');
    const [STInfo, setSTInfo] = useState({ md5: '', sha256: '' });
    const [currentEvalResult, setCurrentEvalResult] = useState(eval_result_status[0]);
    const [evalResultPassFailNums, setEvalResultPassFailNums] = useState([0, 0, 0, 0]);
    const [selectedResult, setSelectedResult] = useState(null);
    const [evalResults, setEvalResults] = useState([]); // Evaluation results should contain 1.name 2.status(pass or fail) 3.detail explain of the result

    useEffect(() => {
        const get_st = async () => {
            const token = window.localStorage.getItem("access_token");
            try {
                const user_st = await get_user_st();
                if(user_st) {
                    setUserST(user_st.data);
                    setLoading(false);
                }
            }
            catch(error) {
                console.log("error");
            }
            console.log(userST);
        }

        get_st();
    }, [])


    // Logout initialization function
    const logOut = () => {
        window.localStorage.setItem("access_token", null);
        window.localStorage.setItem("username", null);
        window.localStorage.setItem("user_id", null);
        setAlert(1);
        setMode(0);
    }
    const setting = () => {
        setMode(3);
    }

    // Upload ST handling function
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
                    <button className="main_app_navbar_button">
                        <i className="fa-solid fa-user"></i>
                        <div className="dropdown-wrapper">
                            {/* User Security Target select section */}
                            <div className="dropdown-content">
                                <button><pre>◀  History ST</pre></button>
                                <div className="user_st_lists">
                                    {userST && userST.map((st, index) => (
                                        <div className="user_st_list_item" key={index}>
                                            <button><pre>{st.st_name}</pre></button>
                                        </div>
                                    ))}
                                </div>
                            </div>
                            {/* User settings button */}
                            <div className="dropdown-content">
                                <button onClick={setting}><pre>Setting</pre></button>
                            </div>
                            {/* User log out button */}
                            <div className="dropdown-content">
                                <button onClick={logOut}><pre>Log out</pre></button>
                            </div>
                        </div>
                    </button>
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
            
            <div className="footer_btn_group">
                <button className="save_evaluation_result_btn">
                    <i class="fa-solid fa-floppy-disk"></i> Save
                </button>
                <button className="save_evaluation_result_btn">
                <i class="fa-solid fa-download"></i> Download
                </button>
            </div>
        </div>
    )
};

export default MainApp;