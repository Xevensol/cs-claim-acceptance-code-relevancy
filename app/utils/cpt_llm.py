from typing import List, Optional

from langchain_core.output_parsers import PydanticOutputParser

from app.schemas.schema import Codes
from app.core.connection import get_icd_descriptions
from app.services.prompts.relevancy_prompt import get_relevancy_prompt
from app.services.llm_service import get_chain
from app.utils.logger import get_logger

logger = get_logger(__name__)


def evaluate_codes(codes: dict) -> Optional[Codes]:
    """
    Evaluates code relevance using LLM.

    Args:
        codes (dict): Dictionary containing 'icd_10' and 'sbs_code' lists with summaries.

    Returns:
        Optional[Codes]: Parsed LLM output or None on failure.
    """
    try:
        content_prompt = get_relevancy_prompt()
        parser = PydanticOutputParser(pydantic_object=Codes)
        chain = get_chain(content_prompt, parser)
        response = chain.invoke({"codes": codes})
        return response
    except Exception as e:
        logger.error(f"Error evaluating codes: {e}", exc_info=True)
        return None


def get_code_description(codes: str) -> Optional[dict]:
    """
    Retrieves code descriptions from the database.

    Args:
        codes (str): Comma-separated string of code values.

    Returns:
        Optional[dict]: Dictionary containing descriptions or None on failure.
    """
    try:
        return get_icd_descriptions(codes)
    except Exception as e:
        logger.error(f"Error fetching code descriptions: {e}", exc_info=True)
        return None


def get_relevant_codes(cpt_codes: List[str], irrelevant_codes: List[str]) -> List[str]:
    """
    Filters out irrelevant CPT codes.

    Args:
        cpt_codes (List[str]): List of all CPT codes.
        irrelevant_codes (List[str]): List of codes to exclude.

    Returns:
        List[str]: Filtered list of relevant codes.
    """
    try:
        irrelevant_set = {code.strip() for code in irrelevant_codes}
        return [code for code in cpt_codes if code.strip() not in irrelevant_set]
    except Exception as e:
        logger.error(f"Error filtering relevant codes: {e}", exc_info=True)
        return []
