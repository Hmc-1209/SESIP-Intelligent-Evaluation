import openai
import os
from dotenv import load_dotenv
import pdfplumber

load_dotenv()


def pdf_to_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def evaluate(st_file_path):

    try:
        sesip_methodology = open("./prompt/SESIP_Methodology.txt", 'r', encoding='utf-8').read()
        sesip_evaluation_report = open("./prompt/SESIP_Evaluation_Report.txt", 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"Failed with error {e}")
        return False
    
    st = pdf_to_text(st_file_path)
    openai.api_key = os.getenv("API_KEY")

    prompt = '''
    The following information will contain three files' context for you to evaluate.
    The first one will be the SESIP methodology to let you understand how SESIP works.
    The second one will be the SESIP evaluation report to let you know what to focus for evaluation.
    The third one will be the target of evaluation.
    I want you to understand them and help me evaluate the target with the first two files' rules.
    
    In the second file, you will get a lot of "work units" for different level of SESIP.
    I want your reply contains these details, with the format I give you:
    
    ------Response format starts------
    {
        TOE_Name: "",
        Developer_Organization: "",
        SESIP_Level: "",
        Work_Units: [
            {
                Work_Unit_Name: "",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            ...
        ],
        SFRs_SARs_Evaluation_Result_Status: [...]
    }
    ------Response format ends------
    
    Response format description:
    The TOE_Name, Developer_Organization and SESIP_Level should be considered first.
    In Work_Units, there should be the same amount of objects as the Work_Units in the corresponding SESIP_Level,decided by the SESIP_evaluation_report section.
    In each of these Work_Units objects, the Work_Unit_Name should be the name of the work unit itself (ex: ASE_INT.1-1).
    In each of these Work_Units objects, the Work_Unit_Description should be why the targeting Security Target meets the requirement of the work unit (or not) and why, along with where the information could be found (if possible), try being as detail as possible.
    In each of these Work_Units objects, the Work_Unit_Evaluation_Result_Status should contain only a simple string with "pass" or "fail" reguarding the evaluation result of the corresponding work unit.
    The SFRs_SARs_Evaluation_Result_Status should contain for values, in the order of passed_SFRs, failed_SFRs, passed_SARs, failed_SARs.
    
    The following document is the SESIP methodology.
    ------SESIP Methodology starts------
    ''' + sesip_methodology + '''
    ------SESIP Methodology ends------
    
    The following document is the sesip evaluation report.
    ------SESIP Evaluation Report starts------
    ''' + sesip_evaluation_report + '''
    ------SESIP Evaluation Report ends------
    
    Te following document is the targeting Security Target.
    ------Targeting Security Target starts------
    ''' + st + '''
    ------Targeting Security Target ends------
    
    Please give me the response using the above given rules.
    '''

    try:
        response = openai.completions.create(
            engine="gpt-4o",
            prompt=prompt,
            max_tokens=20000,
            temperature=0.7
        )
        print(response)
    except Exception as e:
        print(f"Failed with error {e}")


evaluate("...")
