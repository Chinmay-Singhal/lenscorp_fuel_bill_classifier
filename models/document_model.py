from typing import Optional, Union, Any
from pydantic import BaseModel


class DocumentModel(BaseModel):
    amount: Optional[Union[int, float, str]]
    date: Optional[Union[int, float, str]]
    volume: Optional[Union[int, float, str]]
    time: Optional[Union[int, float, str]]
