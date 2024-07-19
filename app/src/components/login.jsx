import React, { useContext, useEffect } from "react";
import { AppContext } from "../App";
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

import "./css/login.css";
import get_access_token from "../requests/login_requests";

const LogIn = () => {
  // LogIn component will be rendered when clicking Admin section on home page

  let { alert, setAlert, setMode, setLoading } = useContext(AppContext);
  const error = (error_message) => toast.error(error_message);
  const warn = (warn_message) => toast.warn(warn_message);
  const success = (success_message) => toast.success(success_message);
 
  const loggingIn = async () => {
    // Log In and set the localStorage datas
    setLoading(0);
    const username = document.getElementById("username_input").value;
    const password = document.getElementById("password_input").value;
    if (username === "" || password === "") {
      setLoading(false);
      error("Incomplete login credentials.");
      return;
    }

    const response = await get_access_token(username, password);
    setLoading(false);
    if (response === 1) {
      setMode(2);
    } else if (response === "Username or password incorrect.") {
      error("Incorrect username or password.");
    }
  };

  // Check if the user is logging out
  useEffect(() => {
    switch (alert) {
      case 1:
        warn("You've been logged out.");
        break;
      case 2:
        success("User successfully created!");
        break;
    }

    setAlert(0);
  }, [])

  return (
    <div className="LogInPage">
      <form className="LogInView" onSubmit={loggingIn}>
        <div className="LogInFormTitle">Login</div>

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
        </div>

        <button className="signup_hint" onClick={() => setMode(1)} type="button">Sign Up</button>
        
        {/* Submit button */}
        <button className="LogInFormButton" onClick={loggingIn} type="button">
          Login
        </button>
        <ToastContainer theme="colored" className="alert" limit={1} autoClose={2000}/>
      </form>
    </div>
  );
};

export default LogIn;