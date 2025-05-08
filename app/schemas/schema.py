from pydantic import BaseModel
from typing import List, Optional


class Codes(BaseModel):
    """The class is used to convert LLM output in a structured format"""
    irrelevant_sbs_codes: Optional[List[str]]
    relevant_sbs_codes: Optional[List[str]]
    reason_for_irrelevancy : Optional[str]


class EvaluationInputSchema(BaseModel):
    icd_codes: list[str]
    sbs_codes: list[str]