def st_detail_placeholder(md5):

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
        MD5  :  {md5} 
        SHA256  :  
    </pre>
    """
