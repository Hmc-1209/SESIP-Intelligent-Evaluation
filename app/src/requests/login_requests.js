import axios from "axios";
import { ip } from "./request_host_up";


/* Request behaviors with access token */
const get_access_token = async (user_name, user_password) => {
    // Get the access token for user to verify credential
  
    const formData = new FormData();
    formData.append("username", user_name);
    formData.append("password", user_password);
  
    try {
      const response = await axios.post(`${ip}/token`, formData, {
        headers: {
          accept: "application/json",
          "Content-Type": "application/x-www-form-urlencoded",
        },
        validateStatus: function (status) {
          return (status >= 200 && status < 300) || status === 404;
        },
      });
      if (response.data.access_token) {
        window.localStorage.setItem("access_token", response.data.access_token);
        return 1;
      } else {
        return response.data.detail;
      }
    } catch (error) {
      console.log(error);
    }
    return 5;
};
export default get_access_token;


/* Request behaviors for validating access token */
export const validate_access_token = async (
    access_token = window.localStorage.getItem("access_token")
  ) => {
    // Verify if the access token is not expired
    try {
      const response = await axios.post(
        `${ip}/token/validate_access_token?token=${access_token}`,
        {
          headers: {
            accept: "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
          },
          validateStatus: function (status) {
            return status >= 200 && status < 300;
          },
        }
      );
      if (response.status === 200) {
        return null;
      }
      return response.detail;
    } catch (error) {
      if (error.response && error.response.status === 403) {
        console.log(error.response.data);
      }
    }
    return false;
};


/* Resuest behaviors for sign up */
export const regist_new_user = async (
    user_name,
    user_password,
    user_password_confirm
  ) => {
    // Regist new user using given user_name and password
    if (user_password !== user_password_confirm) {
      return 3;
    }
  
    const body = {
      username: user_name,
      password: user_password,
    };
    console.log(JSON.stringify(body))
  
    try {
      const response = await axios.post(
        `${ip}/user`,
        JSON.stringify(body),
        {
          headers: {
            accept: "application/json",
            "Content-Type": "application/json",
          },
  
          validateStatus: function (status) {
            return (status >= 200 && status < 300) || status === 400;
          },
        }
      );
      if (response.status === 201) {
        return response.status;
      } else if (response.data.detail === "Data Duplicated.") {
        return "Data Duplicated.";
      }
    } catch (error) {
      if (error.response && error.response.status === 403) {
        return 5;
      }
    }
};
