from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

class TextRequest(BaseModel):
    text: str
    
#@app.post("/api/v2/keyword")
#def text_keyword_model():