"""AutoDocEval - Document evaluation and improvement in a closed-loop cycle."""

__version__ = "0.1.0"

from .auto_improve import auto_improve_document
from .compare import compare_documents
from .evaluator import evaluate_document
from .improver import improve_document

__all__ = [
    "auto_improve_document",
    "compare_documents",
    "evaluate_document",
    "improve_document",
]
