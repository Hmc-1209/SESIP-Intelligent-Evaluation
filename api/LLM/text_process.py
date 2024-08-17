import json

import pdfplumber


def api_text_structure(text: str) -> dict:
    return {
        "type": "text",
        "text": text
    }


class Text:
    def __init__(self):
        self._sesip_methodology = open("../api/LLM/prompt/SESIP_Methodology.txt", 'r', encoding='utf-8').read()
        self._sesip_evaluation_report_1_and_2 = open("../api/LLM/prompt/SESIP_Evaluation_Report_Level_1_&_2.txt", 'r',
                                                     encoding='utf-8').read()

        self._int_and_obj = open(f"../api/LLM/prompt/ASE_INT.1_&_ASE_OBJ.1.txt", 'r', encoding='utf-8').read()
        self._req = open("../api/LLM/prompt/ASE_REQ.3.txt", 'r', encoding='utf-8').read()
        self._tss = open("../api/LLM/prompt/ASE_TSS.1.txt", 'r', encoding='utf-8').read()
        self._flr = open("../api/LLM/prompt/ALC_FLR.2.txt", 'r', encoding='utf-8').read()
        self._work_units = json.load(open("../api/LLM/prompt/Work_Units_Lv1_and_2.json", 'r', encoding='utf-8'))
        self._mapping = {0: {"name": "ASE_INT.1_&_ASE_OBJ.1", "rule": self._int_and_obj},
                         1: {"name": "ASE_REQ.3", "rule": self._req},
                         2: {"name": "ASE_TSS.1", "rule": self._tss},
                         3: {"name": "ALC_FLR.2", "rule": self._flr}}

        self._st = ""
        self._sesip_level = 1
        self._step = 0
        self._prompt = {}

    @property
    def prompt(self):
        return self._prompt

    def update_st(self, st_path: str, sesip_level: int):
        self._sesip_level = sesip_level
        self._pdf_to_text(st_path)
        self._step = 0

    def _pdf_to_text(self, st_path: str):
        with pdfplumber.open(st_path) as pdf:
            self._st = "\n".join([x.extract_text() for x in pdf.pages])

    # Evaluate for ST info and work unit's information position
    def get_evaluation_info(self):
        work_units_dict = {unit: "" for unit_list in self._work_units.values() for unit in unit_list}

        self._prompt = api_text_structure(f'''
            I will give you two files' content, I need you to help me provide the information extracted from the targeting Security Target.
            The first one will be the SESIP evaluation report rules.
            The second one will be the targeting security target.
            I want you to understand them and help me get the desired information in the targeting Security Target.
    
            The following document is the SESIP level{self._sesip_level} evaluation report.
            ------SESIP Evaluation Report starts------
            ''' + self._sesip_evaluation_report_1_and_2
                                          + self._int_and_obj
                                          + self._req
                                          + self._tss
                                          + self._flr + '''
            ------SESIP Evaluation Report ends------
    
            The following document is the targeting Security Target.
            ------Targeting Security Target starts------
            ''' + self._st + f'''
            ------Targeting Security Target ends------
    
            In the first file, you will get many "work units".
            I want your response contains these details, with the format I give you:
            ------Response format starts------
            {{
                TOE_Name: "",
                Developer_Organization: "",
                Work_Units_Information_Position: {work_units_dict}
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
    def get_text_content(self, information_position: dict):
        work_units_result = [
            {
                "Work_Unit_Name": unit,
                "Work_Unit_Description": "",
                "Work_Unit_Evaluation_Result_Status": ""
            } for unit in self._work_units[self._mapping[self._step]["name"]]
        ]

        self._prompt = api_text_structure('''
            I will give you three files' content, I need you to help me evaluate the targeting Security Target.
            The first one will be the SESIP methodology.
            The second one will be the SESIP evaluation report rules.
            The third one will be the target of evaluation.
            I want you to understand them and help me evaluate the targeting Security Target with the first two files' rules.
    
            The following document is the SESIP methodology.
            ------SESIP Methodology starts------
            ''' + self._sesip_methodology + f'''
            ------SESIP Methodology ends------
    
            The following document is the SESIP level{self._sesip_level} evaluation report.
            ------SESIP Evaluation Report starts------
            ''' + self._sesip_evaluation_report_1_and_2 + self._mapping[self._step]["rule"] + '''
            ------SESIP Evaluation Report ends------
    
            The following document is the targeting Security Target.
            ------Targeting Security Target starts------
            ''' + self._st + f'''
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

        self._step += 1
