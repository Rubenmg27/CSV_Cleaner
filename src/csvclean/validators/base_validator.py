from abc import ABC, abstractmethod

from csvclean.models.config import Configuration
from csvclean.models.data_register import LineError


class BaseValidator(ABC):

    @abstractmethod
    def validate_line(self, line: list[str], config: Configuration) -> LineError: ...

