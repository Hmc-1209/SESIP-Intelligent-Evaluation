import pdfplumber
import json

sesip_methodology = open("../api/LLM/prompt/SESIP_Methodology.txt", 'r', encoding='utf-8').read()

sesip_evaluation_report_1_and_2 = open(f"../api/LLM/prompt/SESIP_Evaluation_Report_Level_1_&_2.txt", 'r',
                                 encoding='utf-8').read()
ase_int_and_ase_obj = open(f"../api/LLM/prompt/ASE_INT.1_&_ASE_OBJ.1.txt", 'r',
                                 encoding='utf-8').read()
ase_req = open(f"../api/LLM/prompt/ASE_REQ.3.txt", 'r',
                                 encoding='utf-8').read()
ase_tss = open(f"../api/LLM/prompt/ASE_TSS.1.txt", 'r',
                                 encoding='utf-8').read()
alc_flr = open(f"../api/LLM/prompt/ALC_FLR.2.txt", 'r',
                                 encoding='utf-8').read()
work_units = open("../api/LLM/prompt/Work_Units_Lv1_and_2.json", 'r',
                                 encoding='utf-8').read()

def pdf_to_text(pdf_path: str):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def api_text_structure(text: str) -> dict:
    return {
        "type": "text",
        "text": text
    }


# Evaluate for ST info and work unit's information position
def get_evaluation_info(pdf_path: str, sesip_lv: int) -> dict[str, str]:
    """
    The evaluation for ST information and each work unit's information position.

    Args:
        pdf_path (string): The targeting ST file path.
        sesip_lv (int): The desired SESIP evaluation level.

    Returns:
        json data with the format s follow:
        {
            "TOE_Name": "",
            "Developer_Organization": "",
            "Work_Units_Information_Position": [
                {"ASE_INT.1-1": ""},
                {"ASE_INT.1-2": ""},
                {"...": ""}
            ]
        }
    """

    st = pdf_to_text(pdf_path)

    work_units_list = [
        {unit: ""} for key in ["ASE_INT.1_&_ASE_OBJ.1", "ASE_REQ.3", "ASE_TSS.1", "ALC_FLR.2"]
        for unit in work_units[key]
    ]   

    return api_text_structure(f'''
        I will give you two files' content, I need you to help me provide the information extracted from the targeting Security Target.
        The first one will be the SESIP evaluation report rules.
        The second one will be the targeting security target.
        I want you to understand them and help me get the desired information in the targeting Security Target.

        The following document is the SESIP level{sesip_lv} evaluation report.
        ------SESIP Evaluation Report starts------
        ''' + sesip_evaluation_report_1_and_2 
            + ase_int_and_ase_obj
            + ase_req
            + ase_tss
            + alc_flr + '''
        ------SESIP Evaluation Report ends------

        The following document is the targeting Security Target.
        ------Targeting Security Target starts------
        ''' + st + f'''
        ------Targeting Security Target ends------

        In the first file, you will get many "work units".
        I want your response contains these details, with the format I give you:
        ------Response format starts------
        {{
            TOE_Name: "",
            Developer_Organization: "",
            Work_Units_Information_Position: {work_units_list}
        }}
        ------Response format ends------            
                  
        Response format description:  
            TOE_Name: 
                Please evaluate and put the target ST file's TOE name here.
            
            Developer Organization: 
                Please evaluate and put the developer organization name here.
            
            Work_Units_Information_Position: 
                This is an array with all the work_units that is about to be evaluated. Fill in all the information in each work unit where the relative information could be found (at which Section and which page, better with which line).
                For ASE_INT.1-1, write down where the ST reference, TOE reference, TOE overview and TOE description could be found (at which section and which page, better also at which line).
                For ASE_INT.1-2, write down where the ST reference could be found (at which section and which page, better also at which line).
                For ASE_INT.1-3, write down where the TOE reference could be found (at which section and which page, better also at with which line).
                ...etc.

        Please make sure every objects in Work_Units_Information_Position is not empty.
        If the desired information could not be found, write down "The desired information could not be found in the ST".
        
        Make sure the response contains only the json data (without code block format) following the format section above, no other texts outside of it. 
        Check that every strings should be wrapped in double quotation mark.
    ''')


# Evaluate for work units evidence
def get_text_content(pdf_path: str, sesip_lv: int, work_unit_group: int, information_position: dict) -> dict[str, str]:
    """
    The evaluation for specific work units group.

    Args:
        pdf_path (string): The targeting ST file path.
        sesip_lv (int): The desired SESIP evaluation level.
        work_unit_group (int): The work unit group (to know which group of work units it is going to evaluate).
        information_position (dict): The position of each work unit critical information located at, for example,
                                  "ST reference can be found at title page, TOE reference can be found at...".
                                  It is a dict that each work unit key contains a string value for the position.
    Return:
        json data with the format s follow:
        {
            Evaluation_Result: [
                {"Work_Unit_Name": "ALC_FLR.2-1", "Work_Unit_Description": "", "Work_Unit_Evaluation_Result_Status": ""},
                {"Work_Unit_Name": "ALC_FLR.2-2", "Work_Unit_Description": "", "Work_Unit_Evaluation_Result_Status": ""},
                {"...": ""}
            ]
        }
    """

    st = pdf_to_text(pdf_path)

    # Work units' content
    work_units_rules = [ase_int_and_ase_obj, ase_req, ase_tss, alc_flr]

    # Work units' name
    match work_unit_group:
        case 1:
            work_units_result = [
                {
                    "Work_Unit_Name": unit,
                    "Work_Unit_Description": "",
                    "Work_Unit_Evaluation_Result_Status": ""
                } for unit in work_units["ASE_INT.1_&_ASE_OBJ.1"]
            ] 
        case 2:
            work_units_result = [
                {
                    "Work_Unit_Name": unit,
                    "Work_Unit_Description": "",
                    "Work_Unit_Evaluation_Result_Status": ""
                } for unit in work_units["ASE_REQ.3"]
            ] 
        case 3:
            work_units_result = [
                {
                    "Work_Unit_Name": unit,
                    "Work_Unit_Description": "",
                    "Work_Unit_Evaluation_Result_Status": ""
                } for unit in work_units["ASE_TSS.1"]
            ] 
        case 4:
            work_units_result = [
                {
                    "Work_Unit_Name": unit,
                    "Work_Unit_Description": "",
                    "Work_Unit_Evaluation_Result_Status": ""
                } for unit in work_units["ALC_FLR.2"]
            ] 
        
        
    return api_text_structure('''
        I will give you three files' content, I need you to help me evaluate the targeting Security Target.
        The first one will be the SESIP methodology.
        The second one will be the SESIP evaluation report rules.
        The third one will be the target of evaluation.
        I want you to understand them and help me evaluate the targeting Security Target with the first two files' rules.

        The following document is the SESIP methodology.
        ------SESIP Methodology starts------
        ''' + sesip_methodology + f'''
        ------SESIP Methodology ends------

        The following document is the SESIP level{sesip_lv} evaluation report.
        ------SESIP Evaluation Report starts------
        ''' + sesip_evaluation_report_1_and_2 + work_units_rules[work_unit_group - 1] + '''
        ------SESIP Evaluation Report ends------

        The following document is the targeting Security Target.
        ------Targeting Security Target starts------
        ''' + st + f'''
        ------Targeting Security Target ends------

        If you meet some texts like "From SESIP 1" or "As per ...", replace it with corresponding text. Do not just skip it.

        To evaluate the given work units, here's some reference position for the corresponding information:
        f{information_position}   

        In the second file, you will get many "work units".
        I want your response contains these details, with the format I give you:
        ------Response format starts------
        {{   
            Evaluation_Result: {work_units_result}
        }}
        ------Response format ends------

        
        *Important notes!!!*
        If you provide a description of how the work unit were satisfied, also provide where did you find the information, detailed to which page, which section and (if possible), which line.
        If there's any lack of information (no matter it is a outer link, outer reference) as long as it cannot directly shows the sufficient information, the work unit should be marked as fail!!!!!
        Do not reference any documents or knowledge on internet. Just evaluate the target with the information I give you.
        Outer reference's name contain related information cannot be considered provide the needed information, as it did not show the detail!!!!!
        *Important notes!!!*

        Response format description:
            Work_Unit_Description:
            If there is lack of information, or any single part of rules that cannot be directly seen in the ST, do not blindly guess the answer even if the ST provide the outer link or reference, just mark it as fail. All information should be provided clearly for people to directly seen.
            In each of these Work_Units objects, the Work_Unit_Description should not only state whether the targeted Security Target meets the requirements of the work unit but also provide detailed reasoning. Specifically, the response for each work unit should include:
                Why the requirements of that work unit are met or not met, with a clear explanation of the factors contributing to this conclusion, also providing the evidence!
                Precise references to the Security Target (ST) document, including the page number, paragraph, and if possible, the line number where the relevant information(evidence) can be found.
                If the work unit is partially met, describe which aspects are fulfilled and which are lacking, with corresponding references in the ST.
                A brief quoted excerpt from the relevant section of the ST document to support the evaluation, using ... to truncated the quoted evidence of the string is more then 30 characters.    
            Please ensure the explanation is thorough, identifying exact locations in the ST document to support the evaluation. The explanation of why the work unit pass or fail should be detailed. For example why the information being found could prove the work unit requirement have been met.
            At the end of each work unit description, there should be a statement like 'thus, the evaluator confirms it meet all requirements for content and presentation evidence' if the evaluation result is pass, similar to failed, there should also a statement to sum up like so.
            (ex. The TOE reference point out the TOE name (TOE_NAME), version (Rev. 2.4), identification code (IDENTIFICATION_CODE) and the type (Secure co-processor platform for embedded systems). The TOE reference had provided sufficient detail, the combination of them makes the TOE uniquely identifiable, thus the evaluator confirms that it meets all requirements for content and presentation evidence.)

            Work_Unit_Evaluation_Result_Status:
            In each of these Work_Units objects, the Work_Unit_Evaluation_Result_Status should contain only a simple string of either 'Pass' or 'Fail' regarding the evaluation result of the corresponding work unit.
        
        Make sure the response contains only the json data (without code block format) following the format section above, no other texts outside of it. 
        Check that every strings should be wrapped in double quotation mark.
        ''')
