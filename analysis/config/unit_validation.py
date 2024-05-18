
from typing import List, Optional
from dataclasses import dataclass
import logging as log
import re

UNIT_REGEX = re.compile(r'([+-]?(?:[0-9]*[.])?[0-9]+)\s*(\w+)')

@dataclass
class MeasurementUnit:
    unit: str
    full_unit_name: Optional[str]
    multiplier: float

    def try_validate(self, input: str) -> float:
        result = UNIT_REGEX.match(str(input))

        if result is None:
            raise ValueError(f'The value must be like "<VALUE> <UNIT>"')
        
        value, unit = result.groups()

        if not unit == self.unit:
            raise ValueError(f'Invalid unit: {unit}. Expected: {self.unit} ({self.full_unit_name})')
        
        return self.multiplier * float(value)
        
    def __str__(self) -> str:
        if self.full_unit_name is None:
            return f'{self.unit}'
        else:
            return f'{self.unit} ({self.full_unit_name})'


def create_unit_validator(allowed_units: List[MeasurementUnit]):
    def unit_validator(input: str) -> float:
        for unit in allowed_units:
            try:
                return unit.try_validate(input)
            except ValueError:
                pass
        
        allowed_units_string = ', '.join([str(unit) for unit in allowed_units])

        log.error(f'Could not match any unit: {allowed_units_string}')
        log.error(f'The pattern value must be like "<VALUE> <UNIT>"')

        raise ValueError(f'Could not match any unit: {allowed_units_string}')
    
    return unit_validator