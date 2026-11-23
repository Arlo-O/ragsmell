"""Registry of the four core detectors."""

from ragsmell.detectors.base import Detector

REGISTRY: dict[str, Detector] = {}


def _register(*detectors: Detector) -> None:
    for detector in detectors:
        REGISTRY.setdefault(detector.id, detector)


from ragsmell.detectors.ap01_prompt_infiltration import PromptInfiltration
from ragsmell.detectors.ap03_provider_lockin import ProviderLockin
from ragsmell.detectors.ap04_monolithic_rag import MonolithicRag
from ragsmell.detectors.ap05_exception_suppression import ExceptionSuppression

_register(PromptInfiltration(), ProviderLockin(), MonolithicRag(), ExceptionSuppression())
ALL = tuple(REGISTRY.values())
