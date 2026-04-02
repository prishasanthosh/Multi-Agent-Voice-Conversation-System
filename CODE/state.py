from typing import List, Optional
from pydantic import BaseModel
class AgentState(BaseModel):
    transcript: Optional[str] = ""
    step_counter: int = 0
    next: str = "realist"  
    agent_trace: List[str] = []
    optimist_agent: Optional[str] = ""
    realist_agent: Optional[str] = ""
    expert_agent: Optional[str] = ""
