from pydantic import BaseModel, Field
from typing import List

class BugResolutionReport(BaseModel):
    """Schema for the final structured JSON/YAML output required by the assessment."""
    bug_summary: str = Field(description="Clear summary of symptoms, scope, and severity.")
    evidence: List[str] = Field(description="Specific log lines or stack trace excerpts proving the bug.")
    repro_steps: List[str] = Field(description="Step-by-step instructions to reproduce the ORIGINAL bug. The final step MUST explicitly state to verify that the application crashes with the specific error.")
    root_cause_hypothesis: str = Field(description="The root-cause hypothesis, including a confidence level.")
    patch_plan: str = Field(description="Files and modules impacted, proposed approach, and potential risks.")
    validation_plan: str = Field(description="Tests to add and regression checks to verify the fix.")
    open_questions: List[str] = Field(description="Any open questions or missing information.")