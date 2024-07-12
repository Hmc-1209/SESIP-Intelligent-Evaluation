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
