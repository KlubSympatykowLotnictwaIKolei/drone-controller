
from dataclasses import dataclass
from .vector3d import Vector3D
from typing import Tuple
from pyproj import Geod

import numpy as np
import math

@dataclass
class PositionGPS:
    latitude: float
    longitude: float
    relative_altitude: float

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.latitude, self.longitude, self.relative_altitude)
    
    def get_shifted_by_ned_vector(self, vector_ned: Vector3D) -> 'PositionGPS':
        distance = np.sqrt(np.power(vector_ned.x, 2) + np.power(vector_ned.y, 2))
        angle = np.arctan2(vector_ned.y, vector_ned.x)

        lon, lat, _ = Geod(ellps="WGS84").fwd(
            lons=self.longitude,
            lats=self.latitude,
            az=math.degrees(angle),
            dist=distance,
        )

        return PositionGPS(
            latitude=lat,
            longitude=lon,
            relative_altitude=self.relative_altitude-vector_ned.z
        )
    
    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]) -> 'PositionGPS':
        tuple = [*tuple, 0]
        return PositionGPS(tuple[0], tuple[1], tuple[2])
    