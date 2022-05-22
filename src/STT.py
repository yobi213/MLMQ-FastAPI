from pydantic import BaseModel

class STT_layout(BaseModel):
    index : str
    text : str
    ch : str

