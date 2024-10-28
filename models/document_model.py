from typing import Optional, Union
from pydantic import BaseModel


class DocumentModel(BaseModel):
    amount: Optional[Union[int, float]]
    date: Optional[Union[int, float, str]]
    volume: Optional[Union[int, float]]
    time: Optional[Union[int, float, str]]
