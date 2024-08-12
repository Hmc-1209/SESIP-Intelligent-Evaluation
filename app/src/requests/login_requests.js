import axios from "axios";
import { ip } from "./request_host_ip";


const get_access_token = async (user_name, user_password) => {
  // Get the access token for user to do actions.
  //  Param: 
  //    user_name: The user's username for login.
  //    user_password: The user's password for login.
  //  Return:
  //    INTEGER: Status for frontend to take actions.
  //    response.data.detail: Detail information for frontend to take actions.
  
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
    return 5;
  }
};
export default get_access_token;


export const validate_access_token = async (
    access_token = window.localStorage.getItem("access_token")
  ) => {
  // Verify if the access token still not expired
  //  Param: 
  //   access_token: The user's access_token to see if it is still available.
  //  Return:
  //    BOOL: Status for frontend to take actions.
  //    response: Detail information for frontend to take actions.

  try {
    const response = await axios.post(`${ip}/token/validate_access_token?token=${access_token}`, {
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
      return response;
    }
    return response.detail;
  } catch (error) {
    return false;
  }
};


export const regist_new_user = async (
    user_name,
    user_password,
    user_password_confirm
  ) => {
  // Verify if the access token still not expired
  //  Param: 
  //   user_name: The new user's username.
  //   user_password: The new user's password.
  //   user_password_confirm: The new user's password, for confirmation usage.
  //  Return:
  //    INTEGER, Detail information for frontend to take actions.
    
  if (user_password !== user_password_confirm) {
    return 3;
  }
  
  const body = {
    username: user_name,
    password: user_password,
  };
  
  try {
    const response = await axios.post(`${ip}/user`, JSON.stringify(body), {
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
