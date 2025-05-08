from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse

from app.utils.cpt_llm import evaluate_codes, get_code_description
from app.utils.logger import get_logger
from app.schemas.schema import EvaluationInputSchema

relevancy_router = APIRouter()
logger = get_logger(__name__)


@relevancy_router.post("/evaluate_codes")
async def check_codes_relevance(codes: EvaluationInputSchema):
    """
    Evaluate the relevance of multiple SBS codes against multiple ICD-10 codes.
    """
    try:
        icd_codes = codes.icd_codes
        sbs_codes = codes.sbs_codes
        logger.info(f"Received ICD codes: {icd_codes}")
        logger.info(f"Received SBS codes: {sbs_codes}")

        codes = {
            "icd_10": [{"code": code} for code in icd_codes],
            "sbs_code": [{"code": code} for code in sbs_codes],
        }

        all_codes = icd_codes + sbs_codes
        codes_string = ",".join(all_codes)
        codes_data = get_code_description(codes_string)

        if not isinstance(codes_data, dict) or "data" not in codes_data:
            logger.error("Failed to fetch code descriptions.")
            raise HTTPException(status_code=500, detail="Failed to fetch code descriptions.")

        summary_dict = {item["code"]: item["summary"] for item in codes_data["data"]}

        for key in codes:
            for code_entry in codes[key]:
                code = code_entry["code"]
                if code in summary_dict:
                    code_entry["summary"] = summary_dict[code]

        logger.info("Calling LLM to evaluate relevance...")
        output = evaluate_codes(codes)

        if output:
            logger.info("Successfully evaluated codes.")
            return JSONResponse(content={"success": True, "data": dict(output)}, status_code=200)
        else:
            logger.warning("LLM evaluation returned no result.")
            return JSONResponse(content={"success": False, "message": "Evaluation failed."}, status_code=500)

    except Exception as e:
        logger.error(f"Error in /evaluate_codes endpoint: {e}", exc_info=True)
        return JSONResponse(
            content={"success": False, "error": str(e)},
            status_code=500
        )
