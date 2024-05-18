
import math

class Angle:
    __radians: float

    @classmethod
    def from_radians(cls, radians: float) -> 'Angle':
        angle = Angle()
        angle.__radians = radians
        return angle
    
    @classmethod
    def from_degrees(cls, degrees: float) -> 'Angle':
        return cls.from_radians(degrees * math.pi / 180)

    def get_radians(self):
        return self.__radians
    
    def get_degrees(self):
        return self.__radians * 180 / math.pi