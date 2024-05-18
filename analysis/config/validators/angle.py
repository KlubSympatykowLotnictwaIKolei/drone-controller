
from analysis.config.unit_validation import MeasurementUnit, create_unit_validator
import math

angle_validator = create_unit_validator([
    MeasurementUnit(
        unit='deg', 
        full_unit_name='degrees', 
        multiplier=math.pi/180,
    ),
    MeasurementUnit(
        unit='rad', 
        full_unit_name='radians', 
        multiplier=1,
    ),
    MeasurementUnit(
        unit='degrees',
        full_unit_name=None,
        multiplier=math.pi/180,
    ),
    MeasurementUnit(
        unit='radians',
        full_unit_name=None,
        multiplier=1,
    ),
])