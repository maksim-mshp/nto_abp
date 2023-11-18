import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:

    PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATABASE_NAME: str = 'sqlite.db'
    DATABASE_URL: str = f'sqlite:///{PROJECT_ROOT}/{DATABASE_NAME}'


config = Config()
