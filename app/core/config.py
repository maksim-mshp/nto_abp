import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    DATABASE_URL: str = f'sqlite:///{PROJECT_ROOT}/sqlite.db'


config = Config()
