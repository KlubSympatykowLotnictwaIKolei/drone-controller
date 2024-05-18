
from typing import Tuple
from dataclasses import dataclass
from scipy.spatial.transform import Rotation

@dataclass
class Attitude:
    roll: float
    pitch: float
    yaw: float

    def as_tuple(self) -> Tuple[float, float, float]:
        return (self.roll, self.pitch, self.yaw)

    @classmethod
    def from_tuple(cls, tuple: Tuple[float, float, float]) -> 'Attitude':
        return Attitude(tuple[0], tuple[1], tuple[2])

    def to_projection_space_rotation(self) -> Rotation:
        # =================== Explanation ===================
        # Aeuronatical Space       | Projection Space
        #                          |
        #       x (forward)        |  ^ z (up)
        #      ^                   |  |  ^ y (forward)
        #     /                    |  | /
        #    /                     |  |/     
        #   +---------> y (right)  |  +---------> x (right)
        #   |                      |  
        #   |                      |  
        #   |                      |  
        #   v z (down)             | 
        #                          
        # Comparing axes side by side we can see
        # x projection = y aeronautical
        # y projection = x aeronautical
        # z projection = -z aeronautical
        # 
        # By substituding names for aeronautical rotation axes we get:
        # x projection = pitch
        # y projection = roll
        # z projection = -yaw
        #
        # Another important thing aside from the axes is the rotation order
        # Mavlink documentation https://mavlink.io/en/messages/common.html#ATTITUDE
        # describes the attitude message as:
        # "The attitude in the aeronautical frame (right-handed, Z-down, Y-right, X-front, ZYX, intrinsic)".
        #
        # This means the rotation order is ZYX aeronautical which is ZXY projection (check corresponding axes).
        # Our final result is:

        return Rotation.from_euler('ZXY', [-self.yaw, self.pitch, self.roll])