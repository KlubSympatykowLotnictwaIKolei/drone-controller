from analysis.config.unit_validation import MeasurementUnit, create_unit_validator

distance_validator = create_unit_validator([
    MeasurementUnit(
        unit='m',
        full_unit_name='meter',
        multiplier=1e0
    ),
    MeasurementUnit(
        unit='cm',
        full_unit_name='centimeter',
        multiplier=1e-2
    ),
    MeasurementUnit(
        unit='mm',
        full_unit_name='millimeter',
        multiplier=1e-3
    ),
    MeasurementUnit(
        unit='um',
        full_unit_name='micrometer',
        multiplier=1e-6
    ),
])