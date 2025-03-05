from fastapi import APIRouter
from typing import List, Dict
from app.utils.cpt_llm import evaluate_codes, get_code_description

router = APIRouter()


@router.post('/evaluate_codes')
def check_codes_relevance(icd_codes: list[str], sbs_codes: list[str]):
    """
    Evaluate the relevance of multiple SBS codes against multiple ICD-10 codes.
    """
    codes = {
                "icd_10": [{"code": code} for code in icd_codes],
                "sbs_code": [{"code": code} for code in sbs_codes],
            }
    all_codes = icd_codes + sbs_codes
    codes_string = ",".join(all_codes)
    codes_data = get_code_description(codes_string)

    if isinstance(codes_data, dict) and 'data' in codes_data:
        summary_dict = {item['code']: item['summary'] for item in codes_data['data']}

        for key in codes:
            for code_entry in codes[key]:
                code = code_entry['code']
                if code in summary_dict:
                    code_entry['summary'] = summary_dict[code]

        output = evaluate_codes(codes)
    # output = evaluate_codes(codes)


    return output