from datetime import datetime
from typing import Dict, List, Optional

from pydantic import BaseModel


class ControleRuleSchema(BaseModel):
    rule: str
    expression: str
    action: str


class ControlGroupSchema(BaseModel):
    expires: Optional[datetime]
    rules: Dict[str, List[ControleRuleSchema]]
