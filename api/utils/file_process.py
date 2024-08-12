from docx import Document
import os
import json

from config import base_path

report_template = Document(os.path.join(base_path, "evaluation_report_template.docx"))

level1 = {"ASE_INT.1-1": {}, "ASE_INT.1-2": {}, "ASE_INT.1-3": {}, "ASE_INT.1-4": {}, "ASE_INT.1-5": {},
          "ASE_INT.1-6": {}, "ASE_INT.1-7": {}, "ASE_INT.1-8": {}, "ASE_INT.1-9": {}, "ASE_INT.1-10": {},
          "ASE_INT.1-11": {}, "ASE_OBJ.1-1": {}, "ASE_REQ.3-1": {}, "ASE_REQ.3-2": {}, "ASE_REQ.3-3": {},
          "ASE_REQ.3-4": {}, "ASE_REQ.3-5": {}, "ASE_REQ.3-6": {}, "ASE_REQ.3-7": {}, "ASE_TSS.1-1": {},
          "ASE_TSS.1-2": {}, "ALC_FLR.2-1": {}, "ALC_FLR.2-2": {}, "ALC_FLR.2-3": {}, "ALC_FLR.2-4": {},
          "ALC_FLR.2-5": {}, "ALC_FLR.2-6": {}, "ALC_FLR.2-7": {}, "ALC_FLR.2-8": {}, "ALC_FLR.2-9": {},
          "ALC_FLR.2-10": {}}

level_unit_mapping = {1: level1}


def generate_eval_report(st_id: int, sesip_level: int):
    save_path = os.path.join(base_path, str(st_id), "eval_file.docx")
    details_path = os.path.join(base_path, str(st_id), "eval_details.json")
    eval_details = json.load(open(details_path, "r"))

    work_units = eval_details["Work_Units"]
    mapping_unit = level_unit_mapping[sesip_level]

    for unit in work_units:
        mapping_unit[unit["Work_Unit_Name"]] = {
            "description": unit["Work_Unit_Description"],
            "status": unit["Work_Unit_Evaluation_Result_Status"]
        }

    p = report_template.paragraphs
    for i in range(len(p)):
        unit_name = p[i].text.split("(")[0].strip()
        if unit_name in mapping_unit.keys():
            try:
                status = p[i + 2].add_run(mapping_unit[unit_name]["status"])
                status.bold = True
                status.font.name = "Times New Roman"

                description = p[i + 3].add_run(mapping_unit[unit_name]["description"])
                description.font.name = "Times New Roman"

            except KeyError:
                print(f"No such work unit: {unit_name}")
                pass

    report_template.save(save_path)
