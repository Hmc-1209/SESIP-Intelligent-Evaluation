def st_detail_placeholder(details: dict[str, str]) -> str:
    """
    Security Detail placeholder function
    This is a placeholder template for displaying ST detail.
    :param details: dictionary with string of keys and string of values, contains the details information for:
        md5 hash,
        sha256 hash,
        TOE name,
        developer's organization,
        evaluation date,
        SESIP level
    :return: string, the markdown contains the information
    """
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
    """
    Evaluation status placeholder function
    The function of displaying the HTML element code for model evaluation status label.
    :param status: integer, the status of the model evaluation, 0 for pending, 1 for pass and 2 for fail
    :return: string, the HTML element code
    """
    match status:
        case 0:
            return "<i><b><div class='evaluation_status'>Pending</div></b></i>"
        case 1:
            return "<i><b><div class='evaluation_status evaluation_status_pass'>Pass</div></b></i>"
        case 2:
            return "<i><b><div class='evaluation_status evaluation_status_fail'>Fail</div></b></i>"


def evaluation_summary_placeholder(sars_pass: str, sars_fail: str, sfrs_pass: str, sfrs_fail: str) -> str:
    """
    Evaluation summary placeholder function
    The function of displaying the Markdown code of evaluation summary part.
    :param sars_pass: string, the number of sars passed
    :param sars_fail: string, the number of sars failed
    :param sfrs_pass: string, the number of sfrs passed
    :param sfrs_fail: string, the number of sfrs failed
    :return: string, the markdown contains the summary information
    """
    return f'''
    ## Evaluation summary
    <div class='st_detail_custom st_summary'>
        <b><div class='st_summary_pass_num'>{sars_pass}</div></b> SARs passed the evaluation.
        <b><div class='st_summary_fail_num'>&ensp;&ensp;&ensp;{sars_fail}</div></b> SARs failed the evaluation.
        <br>
        <b><div class='st_summary_pass_num'>{sfrs_pass}</div></b> SFRs passed the evaluation. 
        <b><div class='st_summary_fail_num'>&ensp;&ensp;&ensp;{sfrs_fail}</div></b> SFRs failed the evaluation.
    </div>
    '''
