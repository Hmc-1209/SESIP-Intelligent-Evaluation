import React, { useContext } from "react";
import { AppContext } from "../App";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import "./css/login.css";
import { regist_new_user } from "../requests/login_requests";

const SignUp = () => {
  // LogIn component will be rendered when clicking Admin section on home page

  let { alert, setAlert, setMode, setLoading } = useContext(AppContext);
  
  const error = (error_message) => toast.error(error_message);

  const signingUp = async () => {
    // Sign Up 
    setLoading(0);
    const username = document.getElementById("username_input").value;
    const password = document.getElementById("password_input").value;
    const password_confirm = document.getElementById("password_confirm_input").value;
    if (username === "" || password === "" || password_confirm === "") {
      error("Incomplete sign up credentials.")
      setLoading(false);
      return;
    }
    if (password !== password_confirm) {
      error("Confirm password not match.")
      setLoading(false);
      return;
    }
    
    const response = await regist_new_user(username, password, password_confirm);

    if (response === 201) {
      setAlert(2);
      setMode(0);
      setLoading(false);
      return;
    } else if (response === "Data Duplicated.") {
      error("This username has been registed.")
      setLoading(false);
      return;
    }
    error("Unknown problem happened. Please try again later.")
    setLoading(false);
    return;
  };


  return (
    <div className="LogInPage">
      <form className="LogInView">
        <div className="LogInFormTitle">Sign Up</div>

        {/* Username input */}
        <div className="LogInFormInputSection">
            <label htmlFor="username_input_label" className="LogInFormLabel">
            Username
            </label>
            <input type="text" className="LogInFormInput" id="username_input" name="username_input" />
        </div>

        {/* Password input */}
        <div className="LogInFormInputSection">
            <label htmlFor="password_input_label" className="LogInFormLabel">
            Password
            </label>
            <input
            type="password"
            name="password_input"
            id="password_input"
            className="LogInFormInput"
            />
            <label htmlFor="password_confirm_input_label" className="LogInFormLabel">
            Confirm Password
            </label>
            <input
            type="password"
            name="password_confirm_input"
            id="password_confirm_input"
            className="LogInFormInput"
            />
        </div>

        <button className="signup_hint" onClick={() => setMode(0)}>Back to Login</button>

        {/* Submit button */}
        <button className="LogInFormButton" onClick={()=>signingUp()} type="button">
          Submit
        </button>
        <ToastContainer theme="colored" className="alert" limit={1} autoClose={2000}/>
      </form>
    </div>
  );
};

export default SignUp;