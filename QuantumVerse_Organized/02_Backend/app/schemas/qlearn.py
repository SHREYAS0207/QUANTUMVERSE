from pydantic import BaseModel, Field
from typing import Any, Optional
class TutorRequest(BaseModel): message:str; mode:str='step_by_step'; context:dict[str,Any]|None=None; conversationId:Optional[str]=None
class SolverRequest(BaseModel): question:str; context:dict[str,Any]|None=None; examMarks:Optional[int]=None
class ExplorerRequest(BaseModel): query:str; context:dict[str,Any]|None=None
