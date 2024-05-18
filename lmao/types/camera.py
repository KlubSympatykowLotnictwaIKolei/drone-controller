
from scipy.spatial.transform import Rotation
from .position_gps import PositionGPS
from dataclasses import dataclass
from .vector3d import Position3D

@dataclass
class Camera3D:
    position: Position3D
    rotation: Rotation
    horizontal_fov: float
    vertical_fov: float
    near_plane: float = 0.01
    far_plane: float = 100.0

    @dataclass
    class Intrinsics:
        horizontal_fov: float
        vertical_fov: float
    
    @dataclass 
    class Extrinsics:
        position: Position3D
        rotation: Rotation

    @classmethod
    def from_intrinsics_and_extrinsics(cls, intrinsics: Intrinsics, extrinsics: Extrinsics) -> 'Camera3D':
        return cls(
            position=extrinsics.position,
            rotation=extrinsics.rotation,
            horizontal_fov=intrinsics.horizontal_fov,
            vertical_fov=intrinsics.vertical_fov,
        )

@dataclass
class CameraGPS:
    position: PositionGPS
    rotation: Rotation
    horizontal_fov: float
    vertical_fov: float
    near_plane: float = 0.01
    far_plane: float = 100.0

    @dataclass
    class Intrinsics:
        horizontal_fov: float
        vertical_fov: float
    
    @dataclass 
    class Extrinsics:
        position: PositionGPS
        rotation: Rotation

    @classmethod
    def from_intrinsics_and_extrinsics(cls, intrinsics: Intrinsics, extrinsics: Extrinsics) -> 'CameraGPS':
        return cls(
            position=extrinsics.position,
            rotation=extrinsics.rotation,
            horizontal_fov=intrinsics.horizontal_fov,
            vertical_fov=intrinsics.vertical_fov,
        )