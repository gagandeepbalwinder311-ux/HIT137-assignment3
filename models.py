\
"""
Model abstractions and concrete model implementations.

"""
from typing import Any, Dict, List, Optional
from dataclasses import dataclass
from PIL import Image

try:
    from transformers import pipeline
except Exception as e:  # transformers not installed or environment offline
    pipeline = None

from utils import AppError, logged, timing, validate_nonempty, LoggingMixin, TimingMixin

@dataclass
class ModelResult:
    raw: Any
    summary: str

class BaseModel(LoggingMixin, TimingMixin):
    """
    Base class for all models. Demonstrates encapsulation via private attrs
    and provides a polymorphic interface via .run().
    """
    def __init__(self, name: str, task: str):
        self._name = name               # encapsulated model name
        self._task = task               # encapsulated task name
        self._pipeline = None           # encapsulated HF pipeline (lazy)

    @property
    def name(self) -> str:
        return self._name

    @property
    def task(self) -> str:
        return self._task

    @property
    def is_loaded(self) -> bool:
        return self._pipeline is not None

    def load(self):
        """
        Lazily load the model pipeline (implemented by subclasses).
        """
        raise NotImplementedError

    def model_info(self) -> str:
        """
        Return a short human-friendly description shown in the GUI.
        Overridden by subclasses.
        """
        return f"{self._name} ({self._task})"

    def run(self, input_data: Any) -> ModelResult:
        """
        Polymorphic method – overridden by subclasses to execute inference.
        """
        raise NotImplementedError

class MySentimentModel(BaseModel):
    """
    Text sentiment analysis using a small, free model.
    Uses multiple decorators: validate_nonempty + logged + timing.
    """
    MODEL_ID = "distilbert-base-uncased-finetuned-sst-2-english"

    def __init__(self):
        super().__init__(name="DistilBERT Sentiment", task="sentiment-analysis")

    def load(self):
        if pipeline is None:
            raise AppError("transformers not installed. Please run: pip install transformers")
        if not self.is_loaded:
            self.log("Loading sentiment pipeline...")
            self._pipeline = pipeline(self.task, model=self.MODEL_ID)

    def model_info(self) -> str:
        return (
            "Task: Sentiment Analysis\n"
            f"Model: {self.MODEL_ID}\n"
            "Output: POSITIVE/NEGATIVE with a confidence score.\n"
        )

    @validate_nonempty("input_data")
    @logged
    @timing("TextSentimentModel.run")
    def run(self, input_data: str) -> ModelResult:
        self.load()
        self.log(f"Running sentiment on: {input_data[:60]}...")
        preds = self._pipeline(input_data)
        # pipeline returns list of dicts like [{'label': 'POSITIVE', 'score': 0.99}]
        if isinstance(preds, list) and preds:
            p = preds[0]
            summary = f"{p.get('label')} ({p.get('score'):.2f})"
        else:
            summary = "No output"
        return ModelResult(raw=preds, summary=summary)

class ImageClassificationModel(BaseModel):
    """
    Image classification using ViT.
    """
    MODEL_ID = "google/vit-base-patch16-224"

    def __init__(self):
        super().__init__(name="ViT Image Classifier", task="image-classification")

    def load(self):
        if pipeline is None:
            raise AppError("transformers not installed. Please run: pip install transformers and Pillow")
        if not self.is_loaded:
            self.log("Loading image-classification pipeline...")
            self._pipeline = pipeline(self.task, model=self.MODEL_ID)

    def model_info(self) -> str:
        return (
            "Task: Image Classification\n"
            f"Model: {self.MODEL_ID}\n"
            "Output: Top-1/Top-N predicted class labels with scores.\n"
        )

    @logged
    @timing("ImageClassificationModel.run")
    def run(self, input_data: str) -> ModelResult:
        """
        input_data is a path to an image file chosen via file dialog.
        """
        self.load()
        self.log(f"Opening image: {input_data}")
        try:
            img = Image.open(input_data).convert("RGB")
        except Exception as e:
            raise AppError(f"Failed to open image: {e}")
        preds = self._pipeline(img)
        # preds like [{'label': 'Egyptian cat', 'score': 0.87}, ...]
        if isinstance(preds, list) and preds:
            p = preds[0]
            summary = f"{p.get('label')} ({p.get('score'):.2f})"
        else:
            summary = "No output"
        return ModelResult(raw=preds, summary=summary)

# Factory to keep GUI decoupled from concrete classes
def get_available_models():
    return {
        "Text – Sentiment (DistilBERT)": MySentimentModel,
        "Image – Classification (ViT)": ImageClassificationModel,
    }
