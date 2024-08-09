import openai
import os
import pdfplumber

from config import base_path, api_key


def pdf_to_text(pdf_file):
    text = ""
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return text


def evaluate(st_id: int, model: str):
    try:
        sesip_methodology = open("../api/LLM/prompt/SESIP_Methodology.txt", 'r', encoding='utf-8').read()
        sesip_evaluation_report = open("../api/LLM/prompt/SESIP_Evaluation_Report.txt", 'r', encoding='utf-8').read()
    except Exception as e:
        print(f"Failed with error {e}")
        return False

    st_path = os.path.join(base_path, str(st_id), "st_file.pdf")
    st = pdf_to_text(st_path)
    openai.api_key = os.getenv("API_KEY")

    prompt = '''
    I will give you three files' content, I need you to help me evaluate the targeting Security Target.
    The first one will be the SESIP methodology.
    The second one will be the SESIP evaluation report rules.
    The third one will be the target of evaluation.
    I want you to understand them and help me evaluate the targeting Security Target with the first two files' rules.
    
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

    If you met some texts like "From SESIP 1" or "As per ...", then replace the txet with corresponding text. Do not just skip it.

    In the second file, you will get many "work units" for different levels of SESIP.
    I want your response contains these details, with the format I give you:
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
        Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status: [...]
    }
    ------Response format ends------
    
    Response format description:
    The TOE_Name, Developer_Organization and SESIP_Level should be considered first, the SESIP Level will affect the amount of elements in Work_Units array.
    
    *Important notes starts*
    A SESIP Level 1 evaluation should contains 42 work units (ASE_INT.1.1~1-11, ASE_OBJ.1-1, ASE_REQ.3-1~3-7, ASE_TSS.1-1~1-2, AGD_OPE.1-1~1-8, AGD_PRE.1-1~1-3, ALC_FLR.2-1~2-10). Make sure the response contain all the work units. Please make sure they are all in the Work_Units array if it is a SESIP Level 1 evaluation. So the sum of the elements in Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status should be 42.
    *Important notes ends*

    Work_Units array:
        Work_Unit_Name:
        In each of these Work_Units objects, the Work_Unit_Name should be the name of the work unit itself (ex: ASE_INT.1-1).
        
        Work_Unit_Description:
        In each of these Work_Units objects, the Work_Unit_Description should not only state whether the targeted Security Target meets the requirements of the work unit but also provide detailed reasoning. Specifically, the response for each work unit should include:
            1. Why the requirements of that work unit are met or not met, with a clear explanation of the factors contributing to this conclusion, also providing the evidence.
            2. Precise references to the Security Target (ST) document, including the page number, paragraph, and if possible, the line number where the relevant information(evidence) can be found.
            3. If the work unit is partially met, describe which aspects are fulfilled and which are lacking, with corresponding references in the ST.
            4. A brief quoted excerpt from the relevant section of the ST document to support the evaluation, using ... to truncated the quoted evidence of the string is more then 30 characters.    
        Please ensure the explanation is thorough, identifying exact locations in the ST document to support the evaluation. The explanation of why the work unit pass or fail should be detailed. For example why the infomation being found could prove the work unit requirement have been met.
        At the end of each work unit description, there should be a statement like 'thus, the evaluator confirms it meet all requirements for content and presentation evidence' if the evaluation result is pass, similar to failed, there should also a statement to sum up like so.
        (ex. The TOE reference point out the TOE name (TOE_NAME), version (Rev. 2.4), identification code (IDENTIFIATION_CODE) and the type (Secure co-processor platform for embedded systems). The TOE reference had provided sufficient detail, the combination of them makes the TOE uniquely identifiable, thus the evaluator confirms that it meets all requirements for content and presentation evidence.)
        
        Work_Unit_Evaluation_Result_Status:
        In each of these Work_Units objects, the Work_Unit_Evaluation_Result_Status should contain only a simple string of either 'pass' or 'fail' regarding the evaluation result of the corresponding work unit.
        No matter the Work_Unit is pass or failed, it sould be listed in the Work_Unit array, not just listing out the passed one.
        
        Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status:
        Before creating the Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status array, count the number of 'pass' and 'fail' statuses in the Work_Units array to ensure that the sum equals the total number of work units.
        The Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status should contain values in the following order: passed_work_unit_numbers, failed_work_unit_numbers.
        Put the passed work unit amounts and failed work unit amounts in the first and second element in the Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status array.
        The two numbers sum should be equal to the amount of overall Work_Units corresponding to the SESIP Level of evaluation.
    The Work_Units array should contain all the work units corresponding to the level of SESIP evaluation!!!
    The sum of elemtents from Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status should also be the same number of Work_Units array!!!

    Make sure the response contains only the json data (without code block format) following the format section above, no other texts outside of it. 
    Check that every strings should be wrapped in double quotation mark.
    '''

    try:
        response = openai.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        response_text = response.choices[0].message.content
        print("Evaluation complete!")

        details_path = os.path.join(base_path, str(st_id), "eval_result.json")
        with open(details_path, "w", encoding="utf-8") as f:
            f.write(response_text)
        print("Response written to evaluation-result.json")

    except Exception as e:
        print(f"Failed with error {e}")
