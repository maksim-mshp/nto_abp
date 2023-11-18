import os
from dataclasses import dataclass


@dataclass(frozen=True)
class Config:

    PROJECT_ROOT: str = '.'
    DATABASE_NAME: str = 'database.db'
    DATABASE_URL: str = f'sqlite:///{PROJECT_ROOT}/{DATABASE_NAME}'


config = Config()
