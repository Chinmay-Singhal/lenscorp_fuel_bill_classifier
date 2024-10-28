import json
from models.document_model import DocumentModel
 

def get_prompt(
):
    return f"""
        Extract the desired information from the following text that was extracted from the image using OCR.

        Return null if the information is not clear or ambiguous.
        Return null if the information is invalid or incorrect.
        Format and convert any dates in DD-MM-YYYY format.
        Do not remove any fields from the JSON schema mentioned:
        
        Extract the relevant information of fuel invoice. The JSON schema is listed below:
        
        {json.dumps(DocumentModel.model_json_schema(), indent=2)}
    """
