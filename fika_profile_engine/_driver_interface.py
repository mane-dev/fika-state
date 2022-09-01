from abc import ABC, abstractmethod

from ._fika_state import FikaSensorState

class Driver(ABC):
    state: FikaSensorState

    @abstractmethod
    def set_water_temp(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def set_water_flow(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def set_water_pressure(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def set_weight(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def move_piston(self) -> FikaSensorState:
        pass

    @abstractmethod
    def tare(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def position_reference(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def log(self, params) -> FikaSensorState:
        pass

    @abstractmethod
    def get_sensor_data(self) -> FikaSensorState:
        pass