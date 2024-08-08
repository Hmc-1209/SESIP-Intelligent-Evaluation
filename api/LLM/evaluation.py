import openai
import os
from dotenv import load_dotenv
import pdfplumber
# from config import api_key

load_dotenv()


def pdf_to_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def evaluate(st_file_path):

    try:
        sesip_methodology = open("api\LLM\prompt\SESIP_Methodology.txt", 'r', encoding='utf-8').read()
        sesip_evaluation_report = open("api\LLM\prompt\SESIP_Evaluation_Report.txt", 'r', encoding='utf-8').read()
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
    
    In the second file, you will get a lot of "work units" for different levels of SESIP.
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
    In Work_Units, there should be the same amount of objects as the Work_Units in the corresponding SESIP_Level, decided by the SESIP_evaluation_report section (For example, under "Work Units for SESIP 1"). So you need to first understand which SESIP Level the present ST wants to evaluate and get the corresponding work units under the SESIP Evaluation Report section.
    In each of these Work_Units objects, the Work_Unit_Name should be the name of the work unit itself (ex: ASE_INT.1-1).
    In each of these Work_Units objects, the Work_Unit_Description should not only state whether the targeted Security Target meets the requirements of the work unit but also provide detailed reasoning. Specifically, the response should include:
    1. Why the requirements are met or not met, with a clear explanation of the factors contributing to this conclusion.
    2. Precise references to the Security Target (ST) document, including the page number, paragraph, and if possible, the line number where the relevant information can be found.
    3. If the work unit is partially met, describe which aspects are fulfilled and which are lacking, with corresponding references in the ST.
    4. A brief quoted excerpt from the relevant section of the ST document to support the evaluation, using ... to indicate where the text has been truncated if necessary.
    Please ensure the explanation is thorough, identifying exact locations in the ST document to support the evaluation. The explanation of why the work unit pass or fail should be detailed. For example why the infomation being found could prove the work unit requirement have been met.
    In each of these Work_Units objects, the Work_Unit_Evaluation_Result_Status should contain only a simple string of either 'pass' or 'fail' regarding the evaluation result of the corresponding work unit.
    No matter the Work_Unit is pass or failed, it sould be listed in the Work_Unit array, not just listing out the passed one.
    The SFRs_SARs_Evaluation_Result_Status should contain values in the following order: passed_work_unit_numbers, failed_work_unit_numbers. Listed the passed and failed work units corresponding to the result from Work_Units array, it should be a number.
    
    Make sure the response contains only the json data (without code block format), no other texts outside of it.

    The following document is the SESIP methodology.
    ------SESIP Methodology starts------
    ''' + sesip_methodology + '''
    ------SESIP Methodology ends------
    
    The following document is the sesip evaluation report.
    ------SESIP Evaaluation Report starts------
    ''' + sesip_evaluation_report + '''
    ------SESIP Evaluation Report ends------
    
    Te following document is the targeting Security Target.
    ------Targeting Security Target starts------
    ''' + st + '''
    ------Targeting Security Target ends------
    
    Please give me the response using the above given rules.
    '''

    try:
        response = openai.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content
        print("Evaluation complete!")
        with open(r"api\LLM\evaluate-result.json", "w", encoding="utf-8") as f:
            f.write(response_text)
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
