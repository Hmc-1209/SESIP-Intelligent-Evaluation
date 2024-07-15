def st_detail_placeholder(details: dict[str, str]) -> str:

    return f"""
    ## Security Target details
    <pre class='st_detail_custom'>
        TOE  :  
        Developer Organization  :  
        Date  :  
        SESIP Level  :  
    </pre>
    ## Checksum
    <pre class='st_detail_custom'>
        MD5  :  {details["md5"]} 
        SHA256  :  {details["sha256"]}
    </pre>
    """


def evaluation_status_placeholder(status: int) -> str:
    match status:
        case 0:
            return "<i><b><div class='evaluation_status'>Pending</div></b></i>"
        case 1:
            return "<i><b><div class='evaluation_status evaluation_status_pass'>Pass</div></b></i>"
        case 2:
            return "<i><b><div class='evaluation_status evaluation_status_fail'>Fail</div></b></i>"
