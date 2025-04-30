from langchain_openai import ChatOpenAI
from langchain_core.prompts.chat import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from app.core.config import settings
from app.core.connection import get_icd_descriptions
from pydantic import BaseModel
from typing import List, Optional
import requests

class Codes(BaseModel):
    """The class is used to convert LLM output in a structured format"""
    irrelevant_sbs_codes: Optional[List[str]]
    relevant_sbs_codes: Optional[List[str]]
    reason_for_irrelevancy : Optional[str]
    # all_codes_relevant: Optional[str]

def evaluate_codes(codes):


    #     prompt = """
    #     You are a medical coding assistant. Your task is to assess the relevance of CPT codes to the provided ICD codes based on their clinical context. For each CPT code, determine if it is relevant to any of the ICD codes, either directly or indirectly (through procedural relationship).

    #     Relevance: A CPT code is relevant if the procedure it represents can be linked to the condition described by the ICD code. This can include both direct relationships and those based on the treatment or diagnostic procedure typically associated with the condition described by the ICD code.
    #     Irrelevance: A CPT code is irrelevant if no clinical or procedural relationship can be identified between the procedure and the condition described by the ICD code.
        
    #      Provide the output in a structured format:
    #     - relevant_cpt_codes: CPT codes that are relevant to the ICD codes, whether directly or indirectly (e.g., based on related procedures). For example: {{"relevant_cpt_codes": ["82088", "36245"]}}
    #     - irrelevant_cpt_codes: CPT codes that are not relevant to the any ICD codes. For example: {{"irrelevant_cpt_codes": ["69436", "86674"]}}

    #     Now, analyze the following input:
    #     {codes}

    # """

    prompt = """
        You are a medical coding assistant with expertise in **SBS codes** and their respective descriptions. 
        SBS codes refer to standardized codes used to represent medical procedures, services, and treatments. These codes are used to categorize healthcare procedures in a structured format for billing, clinical documentation, and procedural tracking. Your task is to analyze **SBS codes** and **ICD-10 codes** to assess their **relevance** based on clinical context and procedural relationships.

        ### Task:
        You are provided with **ICD-10 codes** and **SBS codes** along with their descriptions. Your goal is to evaluate the **SBS codes** for their relevance to the provided **ICD-10 codes**.

        A **SBS code** is considered **relevant** if its description (the medical procedure or service) can be linked to any one of the **ICD-10 codes** based on clinical context, treatment, or diagnostic relationships. This includes both **direct relationships** (e.g., a procedure used to treat a specific condition) and **indirect relationships** (e.g., a procedure typically associated with a condition described by the ICD-10 code). A **SBS code** is considered **irrelevant** if no such clinical or procedural relationship exists, even if the descriptions don't exactly match, but are semantically related.

        ### Relevance Criteria:
            - **Relevant**: If the **SBS code**'s description is linked to any **ICD-10 code** based on clinical or procedural relationships. For example, an SBS code for "brain surgery" would be relevant to an ICD-10 code for "brain tumor," as brain surgery is often used to treat or manage brain tumors.
            - **Irrelevant**: If the **SBS code**'s description does not relate to any **ICD-10 code**, either directly or indirectly. For example, if an SBS code refers to an anesthetic procedure for nerve pain and there is no related diagnosis such as myalgia or neurological disorder in the ICD-10 codes.

        ### Output Format:
        Provide the output in the following structured format:
            - **relevant_sbs_codes**: A list of SBS codes that are relevant to the provided ICD-10 codes, whether directly or indirectly (e.g., based on related procedures). For example: {{"relevant_sbs_codes": ["73350-00-20", "97414-04-00"]}}
            - **irrelevant_sbs_codes**: A list of SBS codes that are not relevant to any ICD-10 codes. For example: {{"irrelevant_sbs_codes": ["73250-00-91", "73350-07-04", "83620-00-10"]}}
            - **reason_for_irrelevancy**: A clear explanation of why the SBS code is irrelevant. For example: {{"reason_for_irrelevancy": "This SBS code is for a procedure not associated with the conditions described in the provided ICD-10 codes. For example, it pertains to a cranial procedure which is not related to musculoskeletal or cardiovascular conditions."}}

        ### Now, analyze the following input:
        {codes}
    """
    


    # removing summary
    # for category in codes:
    #     for item in codes[category]:
    #         item.pop('summary', None) 

    content_prompt = ChatPromptTemplate.from_template(prompt)
    model = ChatOpenAI(
            model='gpt-4o-mini',
            # model='ft:gpt-4o-mini-2024-07-18:xeven-solutions:sbs-codes:B1wWrKWT',
            temperature=0,
            api_key=settings.OPENAI_API_KEY
        )
    parser = PydanticOutputParser(pydantic_object=Codes)
    # parser = StrOutputParser()
    chain = content_prompt | model | parser
    response = chain.invoke({"codes": codes})
    
    return response if response else None

    

def get_code_description(codes):

    try:
        response = get_icd_descriptions(codes)
        
        return response
    
    except Exception as e:
        return None
    

# Add these helper functions at the top with other functions
def get_relevant_codes(cpt_codes, irrelevant_codes):
    """Get list of relevant CPT codes by excluding irrelevant ones"""
    irrelevant_set = set(code.strip() for code in irrelevant_codes)
    return [code for code in cpt_codes if code not in irrelevant_set]