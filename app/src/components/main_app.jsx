import React, { useContext, useEffect, useState } from "react";
import { AppContext } from "../App";
import ReactDropdown from "react-dropdown";
import "react-dropdown/style.css";
import CryptoJS from "crypto-js";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import models from './models.json';
import '@fortawesome/fontawesome-free/css/all.min.css';
import { ColorRing } from 'react-loader-spinner'
import get_user_st, { delete_history_st, get_st_file_content, get_st_info, st_evaluate, upload_st } from "../requests/user_requests";
// For M1 'brew install pkg-config cairo pango'm then 'npm install @react-pdf-viewer/core@3.12.0'

import "./css/main_app.css";

const MainApp = () => {

    // Static variables
    const model_options = models.available_models;
    const eval_result_status = ['Pending', 'Pass', 'Fail'];
    const success = (success_message) => toast.success(success_message);
    const error = (error_message) => toast.error(error_message);

    // Context variables
    let { alert, setAlert, setMode, loading, setLoading } = useContext(AppContext);

    // useState variables
    const [userST, setUserST] = useState(null);
    const [STFile, setSTFile] = useState(null);
    const [STUrl, setSTUrl] = useState('');
    const [STHash, setSTHash] = useState({ md5: '', sha256: '' });
    const [STInfo, setSTInfo] = useState(null);
    const [STInfoDesciption, setSTInfoDescription] = useState(null);
    const [currentSTID, setCurrentSTID] = useState(null);
    const [currentEvalResult, setCurrentEvalResult] = useState(eval_result_status[0]);
    const [evalResultPassFailNums, setEvalResultPassFailNums] = useState([0, 0]);
    const [selectedResult, setSelectedResult] = useState(null);
    const [evalResults, setEvalResults] = useState([]);
    const [isUploadingST, setIsUploadingST] = useState(false);


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

    // Get the current user's STs
    const get_st = async () => {
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
                setSTHash({ md5, sha256 });
            };
            reader.readAsArrayBuffer(file);
        }
    };
    const handleUploadButtonClick = () => {
        setIsUploadingST(true);
        document.getElementById('fileInput').click();
    };

    // Clear the current used st
    const clear_current_st = () => {
        setCurrentEvalResult('Pending');
        setCurrentSTID(null);
        setSTFile(null);
        setSTUrl('');
        setSTHash({ md5: '', sha256: '' });
        setSTInfo(null);
        setEvalResultPassFailNums([0, 0]);
        setEvalResults([]);
        setSelectedResult(null);
        setSTInfoDescription(null);
    }

    // Process evaluation
    const get_evaluate_result = () => {
        setLoading(1);
        const access_token = window.localStorage.getItem("access_token");
        const evaluate_request = async () => {
            const response = await st_evaluate(access_token, currentSTID);
            if (response) {
                setEvalResults(response.eval_details.Work_Units);
                setSTInfoDescription({
                    TOE_Name: response.st_details.TOE_Name,
                    Developer_Organizetion: response.st_details.Developer_Organizetion,
                    SESIP_Level: response.st_details.SESIP_Level
                })
                setEvalResultPassFailNums([response.eval_details.Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status[0], response.eval_details.Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status[1]]);
                setLoading(false);
                setSTInfo(prevSTInfo => ({
                    ...prevSTInfo,
                    is_evaluated: true,
                }));
                setCurrentEvalResult(response.is_valid === true ?
                     'Pass' : 'Fail');
                success("Evaluation comlete!");
                return;
            } else {
                error("Unknown error happend. Try again later.");
                setLoading(false);
                return;
            }
        }
        evaluate_request();
    }

    // Get history st content and detail information
    const get_history_st = async (st_id) => {
        setIsUploadingST(false);
        clear_current_st();
        setLoading(0);
        const access_token = window.localStorage.getItem("access_token");
        const response_info = await get_st_info(access_token, st_id);
        const response_pdf = await get_st_file_content(access_token, st_id);
        setSTUrl(URL.createObjectURL(response_pdf));
        setCurrentSTID(response_info.st_id);
        if (response_info && response_pdf) {
            // If the ST had already been evaluated
            if(response_info.st_details !== null) {
                setEvalResults(response_info.eval_details.Work_Units);
                setSTInfoDescription({
                    TOE_Name: response_info.st_details.TOE_Name,
                    Developer_Organizetion: response_info.st_details.Developer_Organizetion,
                    SESIP_Level: response_info.st_details.SESIP_Level
                })
                setEvalResultPassFailNums([response_info.eval_details.Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status[0], response_info.eval_details.Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status[1]]);
                setCurrentEvalResult(response_info.is_valid === true ? eval_result_status[1] : eval_result_status[2]);
            }
            setSTInfo({is_evaluated: response_info.is_evaluated});
            const reader = new FileReader();
            reader.onload = (e) => {
                const binary = e.target.result;
                const md5 = CryptoJS.MD5(CryptoJS.lib.WordArray.create(new Uint8Array(binary))).toString();
                const sha256 = CryptoJS.SHA256(CryptoJS.lib.WordArray.create(new Uint8Array(binary))).toString();
                setSTHash({ md5, sha256 });
            };
            reader.readAsArrayBuffer(response_pdf);
            setSTFile(response_pdf);
            setLoading(false);
        }
    }

    // Delete specific ST, it should also be the currently selected one
    const delete_history_security_target = async () => {
        setLoading(0);
        const access_token = window.localStorage.getItem("access_token");
        const response = await delete_history_st(access_token, currentSTID);
        if (response) {
            success("Security Target deleted.")
            setLoading(false);
            clear_current_st();
            get_st();
            return;
        }
        error("Unknown problem happend. Try again later.")
        return;
    }


    useEffect(() => {
        
        get_st();
    }, [])

    useEffect(() => {
        const upload_new_st_file = async () => {
            if (STFile.name.split('/').pop().length > 50) {
                error("Filename too long!");
                setSTFile(null);
                setSTUrl('');
                setCurrentSTID(null);
                setSTHash({ md5: '', sha256: '' });
                return;
            }
            const access_token = window.localStorage.getItem("access_token");
            const response = await upload_st(access_token, STFile);
            if (response !== 0 && response !== 'Request failed.') {
                success("Upload success!");
                setCurrentSTID(response);
                get_st();
                const current_st_information = await get_st_info(access_token, response);
                if (current_st_information) {
                    setSTInfo(current_st_information);
                }
                return;
            } else {
                error("Failed to upload.");
                setSTFile(null);
                setSTUrl('');
                setCurrentSTID(null);
                setSTHash({ md5: '', sha256: '' });
                return;
            }
        }
        if (STFile !== null && isUploadingST) {
            upload_new_st_file();
            setIsUploadingST(false);
        }
    }, [STFile])

    
    return (
        <div className="main_app_page">

            {/* Navbar */}
            <div className="main_app_navbar">
                <pre style={{"fontSize":"30px"}}>
                    SESIP Intelligence Eval
                    {/* <div className="main_app_navbar_subtitle">LLM evaluated result will be provided using this tool.</div> */}
                </pre>
                <div className="main_app_navbar_button_group">
                    <div className="main_app_navbar_button">
                        <i className="fa-solid fa-user"></i>
                        <div className="dropdown-wrapper">
                            {/* User Security Target select section */}
                            <div className="dropdown-content">
                                {loading === 1 ?
                                <button disabled><pre>◀  History ST</pre></button> :
                                <button><pre>◀  History ST</pre></button>
                                }
                                <div className="user_st_lists">
                                    {userST && userST.map((st, index) => (
                                        <div className="user_st_list_item" key={index} disabled>
                                            {loading === 1 ?
                                                <button disabled><pre>{st.st_name}</pre></button> :
                                                <button onClick={() => get_history_st(st.st_id)}><pre>{st.st_name}</pre></button>
                                            }
                                        </div>
                                    ))}
                                </div>
                            </div>
                            {/* User settings button */}
                            <div className="dropdown-content">
                                {loading === 1 ?
                                    <button disabled><pre>Setting</pre></button> :
                                    <button onClick={setting}><pre>Setting</pre></button>
                                }   
                            </div>
                            {/* User log out button */}
                            <div className="dropdown-content">
                                {loading === 1 ?
                                    <button disabled><pre>Log out</pre></button> :
                                    <button onClick={logOut}><pre>Log out</pre></button>
                                }
                            </div>
                        </div>
                    </div>
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
                    <button onClick={handleUploadButtonClick} className="st_upload_btn">
                        Upload Security Target
                    </button>
                }
                <div className="main_app_st_section">
                    {STUrl !== '' && 
                        <div className="st_content_display">
                            <object data={STUrl} type="application/pdf" className="st_content" style={{ width: '100%' }}/>
                        </div>
                    }
                    <div className="st_section_right">
                        <div className="st_detail_process">
                            <pre className="st_detail_title">
                                Security Target Details
                            </pre>
                            <pre className="st_detail_information">
                                TOE name : {STInfoDesciption ? STInfoDesciption.TOE_Name : ''}<br /><br />
                                Developer Organization : {STInfoDesciption ? STInfoDesciption.Developer_Organizetion : ''}<br /><br />
                                SESIP Level : {STInfoDesciption ? STInfoDesciption.SESIP_Level : ''}
                            </pre>
                            <pre className="st_detail_title">
                                Checksum
                            </pre>
                            <pre className="st_detail_information">
                                MD5 hash : {STHash.md5}<br /><br />
                                SHA256 hash : {STHash.sha256}
                            </pre>    
                        </div>

                        {/* Model select dropdown list */}
                        <pre className="model_selector_label">Select Model for evaluation :</pre>
                        <ReactDropdown options={model_options} value={model_options[0]} className="model_selector"/>
                        
                        {/* Evaluation button and result */}
                        {((STInfo === null) || (STInfo.is_evaluated !== false) || loading === 1) ? 
                        <button className="process_evaluation_btn" disabled>Evaluate</button> : 
                        <button className="process_evaluation_btn" onClick={get_evaluate_result}>Evaluate</button>}

                        <i><div className={"evaluation_result_label " + 
                                                (currentEvalResult === eval_result_status[0] ? "eval_pending" :
                                                currentEvalResult === eval_result_status[1] ? "eval_pass" :
                                                "eval_fail")
                                        }>
                            {currentEvalResult}
                            {loading === 1 && 
                                <div className="main_app_evaluation_loading_background">
                                    <ColorRing
                                    visible={true}
                                    height="100"
                                    width="100"
                                    ariaLabel="color-ring-loading"
                                    wrapperStyle={{}}
                                    wrapperClass="color-ring-wrapper"
                                    colors={['#5A7D7C', '#DADFF7', '#232C33', '#A0C1D1', '#B5B2C2']}
                                    />
                                </div>
                            }
                        </div></i>
                        <pre className="eval_brief_result">
                            {evalResultPassFailNums[0]} work units passed the evaluation.<br />{evalResultPassFailNums[1]} work units failed the evaluation.<br /><br />
                        </pre>
                    </div>
                </div>
            </div>

            {/* Evaluation result section */}
            <div className="main_app_result_section">
                <div className="result_container">
                    {evalResults.map(result => (
                        <button className={"result_brief_label "+(selectedResult && (selectedResult.Work_Unit_Name===result.Work_Unit_Name)?"selected_result":"")} onClick={() => setSelectedResult(result)} key={result.Work_Unit_Name} style={{display: 'flex'}}>
                            {result.Work_Unit_Evaluation_Result_Status === 'pass' ?
                             <div style={{ color: 'green', fontWeight: 'bold', marginRight: '10px' }}>O</div> :
                             <div style={{ color: 'red', fontWeight: 'bold', marginRight: '10px' }}>X</div>}{result.Work_Unit_Name? result.Work_Unit_Name : "null"}
                        </button>
                    ))}
                </div>
                <div className="result_detail_content">
                    {selectedResult ?
                    <div>
                        {selectedResult.Work_Unit_Description}
                    </div> : "Select result for more information."}
                </div>
            </div>
            
            {/* Footer functional buttons section */}
            <div className="footer_btn_group">
                {(loading === 1) ? 
                <button className="save_evaluation_result_btn" disabled>
                    <i className="fa-solid fa-xmark"></i> Clear
                </button> :
                <button className="save_evaluation_result_btn" onClick={clear_current_st}>
                    <i className="fa-solid fa-xmark"></i> Clear
                </button>
                }
                
                
                {((STInfo === null) || loading === 1) ?
                (<button className="save_evaluation_result_btn" disabled>
                    <i className="fa-solid fa-trash-can"></i> Delete
                </button>
                ) : (
                <button className="save_evaluation_result_btn" onClick={delete_history_security_target}>
                    <i className="fa-solid fa-trash-can"></i> Delete
                </button>)}
                
                {((STInfo === null) || (STInfo.is_evaluated === false)) ?
                <button className="save_evaluation_result_btn" disabled>
                <i className="fa-solid fa-download"></i> Download
                </button> : <button className="save_evaluation_result_btn">
                <i className="fa-solid fa-download"></i> Download
                </button>}
            </div>
            <ToastContainer theme="colored" className="alert" limit={1} autoClose={2000}/>

        </div>
    )
};

export default MainApp;