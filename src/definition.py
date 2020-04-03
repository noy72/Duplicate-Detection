import os

from dataclasses import dataclass

ROOT = os.path.dirname(__file__)


@dataclass
class TABLES:
    test: str = "test"
    production: str = "production"
