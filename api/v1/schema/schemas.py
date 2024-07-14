from uuid import UUID
from pydantic import BaseModel

class Todo_in(BaseModel):
    task: str
    status: bool


class Todo_out(BaseModel):
    id: UUID
