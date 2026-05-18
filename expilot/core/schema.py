from typing import Any, Dict, Optional
from pydantic import BaseModel, Field, model_validator

class ToolCall(BaseModel):
    tool_name: str = Field(..., description="必须与工具名称完全一致")
    arguments: Dict[str, Any] = Field(
        ...,
        description="调用该工具所需的参数字典，必须包含所有必填参数"
    )

class AgentAction(BaseModel):
    thought: str = Field(..., description="简短的推理过程")
    action_type: str = Field(..., description="只能是 'tool' 或 'final'（也接受 'answer'）")
    tool_call: Optional[ToolCall] = None
    final_answer: Optional[str] = None

    model_config = {"extra": "forbid"}

    @model_validator(mode="after")
    def normalize_action_type(self):
        if self.action_type == "answer":
            self.action_type = "final"
        return self
