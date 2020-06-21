from abc import ABC, abstractmethod

from lib.config.config import Config


class AbstractConfigReadWriter(ABC):
    @abstractmethod
    def read(self) -> Config:
        raise NotImplementedError("not implemented")

    @abstractmethod
    def write(self, config: Config) -> bool:
        raise NotImplementedError("not implemented")

