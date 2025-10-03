
\
"""
Extra classes showcasing OOP requirements in isolation from the main models.
"""
from utils import LoggingMixin, TimingMixin, logged, timing

class BaseTool(LoggingMixin, TimingMixin):
    def description(self) -> str:
        return "BaseTool: abstract description."
    @logged
    @timing("BaseTool.compute")
    def compute(self, x: int, y: int) -> int:
        # Simple method to be overridden
        return x + y

class FancyTool(BaseTool):
    """
    Demonstrates method overriding and multiple inheritance in a different context.
    """
    def description(self) -> str:
        # Overriding parent method
        return "FancyTool: adds logging/timing via mixins; overrides description()."
    @logged
    @timing("FancyTool.compute")
    def compute(self, x: int, y: int) -> int:
        # Overriding compute to change behaviour slightly
        self.log("Fancy computation in progress...")
        base = super().compute(x, y)
        return base * 2

def short_demo_text() -> str:
    """
    A short explanation surfaced in the GUI for examiners, without executing anything heavy.
    """
    return (
        "We define BaseTool with mixins (LoggingMixin, TimingMixin) and override compute() in FancyTool. "
        "Both @logged and @timing are applied to show multiple decorators and method overriding clearly."
    )
