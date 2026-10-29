"""题 3：企业知识问答 Agent 的业务装配。core/ 下是与业务无关的 ReAct 内核。"""
from .checks import CHECKS
from .guard import guard, on_incomplete
from .mock import mock_policy
from .prompts import FINISH_PARAMETERS, SYSTEM_PROMPT
from .tools import build_tools

MAX_STEPS = 10
MAX_TOOL_CALLS = 12

__all__ = ["CHECKS", "FINISH_PARAMETERS", "MAX_STEPS", "MAX_TOOL_CALLS", "SYSTEM_PROMPT",
           "build_tools", "guard", "mock_policy", "on_incomplete"]
