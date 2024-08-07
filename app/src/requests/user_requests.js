import axios from "axios";
import { ip } from "./request_host_ip";

const get_user_st = async (access_token) => {
    
    const token = window.localStorage.getItem("access_token");

    try {
        const response = await axios.get(`${ip}/st`, {
          headers: {
            accept: "application/json",
            Authorization: "Bearer " + token
          },
          validateStatus: function (status) {
            return (status >= 200 && status < 300) || status === 404;
          },
        });
        if (response.data) {
          return response;
        } else {
          return false;
        }
      } catch (error) {
        console.log(error);
      }
      return false;
}
export default get_user_st;

export const update_username = async (access_token, new_username) => {
    
  const body = {username: new_username}

  try {
      const response = await axios.patch(`${ip}/user/update_username`, body, {
        headers: {
          accept: "application/json",
          Authorization: "Bearer " + access_token
        },
        validateStatus: function (status) {
          return (status >= 200 && status < 300) || status === 404;
        },
      });
      
      if (response.status === 200) {
        return true;
      } else {
        return false;
      }
    } catch (error) {
      return error.response.data.detail;
    }
}

export const update_password = async (access_token, old_pass, new_pass) => {
  
  const body = {
    old_password: old_pass,
    new_password: new_pass
  }

  try {
      const response = await axios.patch(`${ip}/user/update_password`, body, {
        headers: {
          accept: "application/json",
          Authorization: "Bearer " + access_token
        },
        validateStatus: function (status) {
          return (status >= 200 && status < 300) || status === 404;
        },
      });
      
      if (response.status === 200) {
        return true;
      } else {
        return false;
      }
    } catch (error) {
      return error.response.data.detail;
    }
}

export const upload_st = async (access_token, st_file) => {
  
  const formData = new FormData();
  formData.append('new_st', st_file);

  try {
      const response = await axios.post(`${ip}/st/`, formData, {
        headers: {
          Authorization: "Bearer " + access_token
        },
        validateStatus: function (status) {
          return (status >= 200 && status < 300) || status === 404;
        },
      });
      if (response.data) {
        return response.data;
      } else {
        return false;
      }
    } catch (error) {
      return error.response.data.detail;
    }
}