import axios from "axios";
import { ip } from "./request_host_ip";

const get_user_st = async () => {
    
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

export const get_st_info = async (access_token, st_id) => {
  try {
    const response = await axios.get(`${ip}/st/${st_id}`, {
      headers: {
        accept: "application/json",
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
    console.log(error);
  }
  return false;
}

export const st_evaluate = async (access_token, st_id, model, sesip_level) => {
  console.log(model, sesip_level)
  try {
    const response = await axios.post(`${ip}/eval/${st_id}`, null, {
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + access_token
      },
      params: {
        eval_model: model,
        sesip_level: sesip_level
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
    console.log(error);
  }
  return false;
}

export const get_st_file_content = async (access_token, st_id) => {
  try {
    const response = await axios.get(`${ip}/st/file/${st_id}`, {
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + access_token
      },
      responseType: 'blob',
      validateStatus: function (status) {
        return (status >= 200 && status < 300) || status === 404;
      },
    });
    if (response.headers['content-type'] === 'application/pdf') {
      return response.data;
    } else {
      return false;
    }
  } catch (error) {
    console.log(error);
  }
  return false;
}

export const delete_history_st = async (access_token, st_id) => {
  try {
    const response = await axios.delete(`${ip}/st/${st_id}`, {
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + access_token
      },
      validateStatus: function (status) {
        return (status >= 200 && status < 300) || status === 404;
      },
    });
    if (response.status === 204) {
      return true;
    } else {
      return false;
    }
  } catch (error) {
    console.log(error);
  }
  return false;
}

export const get_st_report_download = async (access_token, st_id, toe_name) => {
  try {
    const response = await axios.get(`${ip}/st/download/${st_id}`, {
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + access_token
      },
      responseType: 'blob',
      validateStatus: function (status) {
        return (status >= 200 && status < 300) || status === 404;
      },
    });
    const url = window.URL.createObjectURL(new Blob([response.data]));
    const link = document.createElement('a');
    link.href = url;

    const contentDisposition = response.headers['content-disposition'];
    console.log( response)
    let fileName = st_id + '-' + toe_name + ' Evaluation Result.docx';

    if (contentDisposition && contentDisposition.indexOf('attachment') !== -1) {
      const fileNameMatch = contentDisposition.match(/filename\*?=['"]?([^;\n]+)['"]?/);
      if (fileNameMatch.length > 1) {
        fileName = decodeURIComponent(fileNameMatch[1].replace(/UTF-8''/, ''));
      }
    }

    link.setAttribute('download', fileName);
    document.body.appendChild(link);
    link.click();

    link.parentNode.removeChild(link);
    return true;
  } catch (error) {
    console.log(error);
    return false;
  }
}