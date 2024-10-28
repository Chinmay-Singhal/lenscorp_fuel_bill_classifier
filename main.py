import os
import cv2
import numpy as np
from time import time
from rapidocr_onnxruntime import RapidOCR
from rapidocr_pdf import PDFExtracter
from groq import Groq
from models.document_model import DocumentModel
from fastapi import FastAPI, File, Form
from fastapi.middleware.cors import CORSMiddleware
from globals import get_prompt
from env import GROQ_API_KEY, MODEL_NAME


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


os.makedirs("uploads", exist_ok=True)
groq = Groq(api_key=GROQ_API_KEY)
ocr = RapidOCR()
pdf = PDFExtracter(dpi=200)


def image_to_text(file_path: str) -> str:
    def postprocess_image(image_path):
        image = cv2.imread(image_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.GaussianBlur(image, (5, 5), sigmaX=1.0)
        image = cv2.addWeighted(image, 1.5, image, -0.5, 0)
        return image

    try:
        processed_image = postprocess_image(file_path)
        cv2.imwrite(file_path, processed_image)
        result, _ = ocr(file_path, cls=True)
        _, text, _ = list(zip(*result))
        return "\n".join(text)
    except Exception as e:
        print(e)
        return "Error in image OCR"


# def pdf_to_text(file_path: str) -> str:
#     try:
#         with open(file_path, "rb") as f:
#             return pdf(f.read())
#     except Exception as e:
#         print(e)
#         return {"error": "Error in PDF OCR"}


def call_groq_api(text: str) -> dict:
    try:
        chat = groq.chat.completions.create(
            messages=[
                {"role": "system", "content": get_prompt()},
                {"role": "user", "content": f"The OCR is given below.\n\n{text}"},
            ],
            model=MODEL_NAME,
            temperature=0,
            stream=False,
            response_format={"type": "json_object"},
        )
        validated_output = DocumentModel.model_validate_json(
            chat.choices[0].message.content
        )

        formatted_output = {
            key: value for key, value in validated_output if value is not None
        }

        return formatted_output
        
    except Exception as e:
        print(e)
        return {"error": "Error in Groq API"}


@app.post("/api/upload")
def image_ocr_api(file: bytes = File(...)):
    file_path = f"uploads/{int(time())}.jpg"
    try:
        with open(file_path, "wb") as f:
            f.write(file)
        ocr_text = image_to_text(file_path)
        result = call_groq_api(ocr_text)
    except Exception as e:
        print(e)
        return {"error": "Error processing image OCR"}
    finally:
        os.remove(file_path)
    return result


# @app.post("/api/upload/pdf")
# def pdf_ocr_api(file: bytes = File(...), doc_type: str = Form(...)):
#     file_path = f"uploads/{int(time())}.pdf"
#     try:
#         with open(file_path, "wb") as f:
#             f.write(file)
#         ocr_text = pdf_to_text(file_path)
#         result = call_groq_api(ocr_text, doc_type)
#     except Exception as e:
#         print(e)
#         return {"error": "Error processing PDF OCR"}
#     finally:
#         os.remove(file_path)
#     return result


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
