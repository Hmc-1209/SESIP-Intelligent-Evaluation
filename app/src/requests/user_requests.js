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