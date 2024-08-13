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


def evaluate(st_id: int, model: str, sesip_lv: int):
    try:
        sesip_methodology = open("../api/LLM/prompt/SESIP_Methodology.txt", 'r', encoding='utf-8').read()
        sesip_evaluation_report = open(f"../api/LLM/prompt/SESIP_Evaluation_Report_Level_{sesip_lv}.txt", 'r', encoding='utf-8').read()   
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
    ''' + sesip_methodology + f'''
    ------SESIP Methodology ends------
    
    The following document is the SESIP level{sesip_lv} evaluation report.
    ------SESIP Evaluation Re starts------
    ''' + sesip_evaluation_report + '''
    ------SESIP Evaluation Report ends------
    
    The following document is the targeting Security Target.
    ------Targeting Security Target starts------
    ''' + st + '''
    ------Targeting Security Target ends------

    If you meet some texts like "From SESIP 1" or "As per ...", replace it with corresponding text. Do not just skip it.

    In the second file, you will get many "work units" for different levels of SESIP.
    I want your response contains these details, with the format I give you:
    ------Response format starts------
    {
        TOE_Name: "",
        Developer_Organization: "",
        Work_Units: [
            {
                Work_Unit_Name: "ASE_INT.1-1",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-2",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-3",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-4",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-5",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-6",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-7",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-8",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-9",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-10",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_INT.1-11",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_OBJ.1-1",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-1",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-2",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-3",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-4",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            }
            {
                Work_Unit_Name: "ASE_REQ.3-5",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-6",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_REQ.3-7",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_TSS.1-1",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ASE_TSS.1-2",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-1",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-2",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-3",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-4",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-5",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-6",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-7",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-8",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-9",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            },
            {
                Work_Unit_Name: "ALC_FLR.2-10",
                Work_Unit_Description: "",
                Work_Unit_Evaluation_Result_Status: ""
            }
            ...
        ]
    }
    ------Response format ends------
    
    Response format description:
    The TOE_Name, Developer_Organization should be considered first, the SESIP Level will affect the amount of elements in Work_Units array.
    
    *Important notes below!!!*
    Work Units like ASE_OPE, ASE_PRE, AVA_VAN do not need to evaluate since there are too many missing information. Just skip these work units.
    If you provide a description of how the work unit were statisfied, also provide where did you find the information, detailed to which page, which seciton and (if possible), which line!!!!!
    Do not reference any documents or knowledges on internet. Just evaluate the target with the information I give you.
    If there's any lack of information (no matter it is a outer link, outer reference) as long as it cannot directly shows the sufficient infomation, the work unit should be marked as fail!!!!!
    Outer reference's name contain related information cannot be considered provide the needed information, as it did not show the detail!!!!!
    *Important notes above!!!*

    
    Work_Unit_Description:
    If there is lack of information, or any single part of rules that cannot be directly seen in the ST, do not blindly guess the answer even if the ST provide the outer link or reference, just mark it as fail. All information should be provided clearly for people to directly seen.
    In each of these Work_Units objects, the Work_Unit_Description should not only state whether the targeted Security Target meets the requirements of the work unit but also provide detailed reasoning. Specifically, the response for each work unit should include:
    - Why the requirements of that work unit are met or not met, with a clear explanation of the factors contributing to this conclusion, also providing the evidence.
    - Precise references to the Security Target (ST) document, including the page number, paragraph, and if possible, the line number where the relevant information(evidence) can be found.
    - If the work unit is partially met, describe which aspects are fulfilled and which are lacking, with corresponding references in the ST.
    - A brief quoted excerpt from the relevant section of the ST document to support the evaluation, using ... to truncated the quoted evidence of the string is more then 30 characters.    
    Please ensure the explanation is thorough, identifying exact locations in the ST document to support the evaluation. The explanation of why the work unit pass or fail should be detailed. For example why the infomation being found could prove the work unit requirement have been met.
    At the end of each work unit description, there should be a statement like 'thus, the evaluator confirms it meet all requirements for content and presentation evidence' if the evaluation result is pass, similar to failed, there should also a statement to sum up like so.
    (ex. The TOE reference point out the TOE name (TOE_NAME), version (Rev. 2.4), identification code (IDENTIFIATION_CODE) and the type (Secure co-processor platform for embedded systems). The TOE reference had provided sufficient detail, the combination of them makes the TOE uniquely identifiable, thus the evaluator confirms that it meets all requirements for content and presentation evidence.)

        
    Work_Unit_Evaluation_Result_Status:
    In each of these Work_Units objects, the Work_Unit_Evaluation_Result_Status should contain only a simple string of either 'Pass' or 'Fail' regarding the evaluation result of the corresponding work unit!!!
    Check the response format again before giving me the answer to make sure that every work unit contains in it.
    The sum of elemtents from Work_Units_Evaluation_Result_Passes_Failed_Numbers_Status should be 31!!!

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
