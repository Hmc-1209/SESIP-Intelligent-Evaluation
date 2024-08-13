import axios from "axios";
import { ip } from "./request_host_ip";


const get_user_st = async (access_token) => {
  //  Get the current user's history Security Targets
  //  Param: 
  //    access_token: The token for doing user actions.
  //  Return:
  //    response: If sccessfully get the user's hisrtory st, return it. 
  //    BOOL: Return false to show there's a problem happened when fetching st.

  try {
    const response = await axios.get(`${ip}/st`, {
      headers: {
        accept: "application/json",
        Authorization: "Bearer " + access_token
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
    return false;
  }
}
export default get_user_st;


export const update_username = async (access_token, new_username) => {
  // Update the user's username
  //  Param: 
  //    access_token: The token for doing user actions.
  //    new_username: The name the user want's to change to.
  //  Return:
  //    error.response.data.detail: The detail error information for frontend to show error message.
  //    BOOL: Whether the update success or not.

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
  // Update the user's password
  //  Param: 
  //    access_token: The token for doing user actions.
  //    old_pass: The old password for user to check the identity once more.
  //    new_pass: The new password the user want's to change to.
  //  Return:
  //    error.response.data.detail: The detail error information for frontend to show error message.
  //    BOOL: Whether the update success or not.

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
  // Uploading the new security target
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_file: The targeting security target file(pdf).
  //  Return:
  //    error.response.data.detail: The detail error information for frontend to show error message.
  //    BOOL: Whether the upload success or not.
  //    response.data: The detaial message for frontend to determine what actions to take.

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
  // Get the current showing security target information
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The targeting security target id.
  //  Return:
  //    BOOL: Whether the get request success or not.
  //    response.data: The detaial message for frontend to determine what actions to take.

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
    return false;
  }
}


export const st_evaluate = async (access_token, st_id, model, sesip_level) => {
  // Evaluate the targeting security target
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The targeting security target id.
  //    model: The LLM model the security target is going to evaluate with.
  //    sesip_level: The desired SESIP level for the evaluation.
  //  Return:
  //    BOOL: Whether the evaluate success or not.
  //    response.data: The detaial message for frontend to determine what actions to take.

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
    return false;
  }
}


export const get_st_file_content = async (access_token, st_id) => {
  // Get the security target file content (pdf file) for display
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The targeting security target id.
  //  Return:
  //    BOOL: Whether the get request success or not.
  //    response.data: The security target file blob data.

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
    return false;
  }
}


export const delete_history_st = async (access_token, st_id) => {
  // Delete the selected securty target evaluation data & files
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The targeting security target id.
  //  Return:
  //    BOOL: Whether the delete success or not.

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
    return false;
  }
}


export const get_st_report_download = async (access_token, st_id, toe_name) => {
  // Delete the selected securty target evaluation data & files
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The targeting security target id.
  //    toe_name: The TOE name to make evaluation result docx file.
  //  Return:
  //    BOOL: Whether the download success or not.

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
    return false;
  }
}


export const get_user_transfer_token = async (access_token) => {
  // Get the current user's transfer token for later use
  //  Param: 
  //    access_token: The token for doing user actions.
  //  Return:
  //    BOOL: Whether the get request success or not.
  //    response.data: The transfer token.

  try {
    const response = await axios.post(`${ip}/token/transfer_token`, {}, {
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
    return false;
  }
}


export const transfer_st = async (access_token, st_id, transfer_token) => {
  // Get the current user's transfer token for later use
  //  Param: 
  //    access_token: The token for doing user actions.
  //    st_id: The target st that it about to be transferred.
  //    transfer_token: The access of transfering st.
  //  Return:
  //    BOOL: Whether the get transfer success or not.
  
  const body = {token: transfer_token};
  console.log(body)

  try {
    const response = await axios.patch(`${ip}/st/${st_id}`, body, {
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
    return false;
  }
}


export const delete_user = async (access_token) => {
  // Delete the current user
  //  Param: 
  //    access_token: The token for doing user actions.
  //  Return:
  //    BOOL: Whether the delete success or not.

  try {
    const response = await axios.delete(`${ip}/user`, {
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
    return false;
  }
}