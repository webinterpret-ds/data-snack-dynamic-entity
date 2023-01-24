from data_snack_dynamic_entity.types import FieldSchema


def key_exclusion_validator(field_name: str, field_schema: FieldSchema) -> None:
    """Raises ValueError if field schema is marked as key and excluded at the same time."""
    if field_schema.get("key") and field_schema.get("excluded"):
        raise ValueError(f"Wrong {field_name} field schema. Key can not be excluded.")


def key_default_validator(field_name: str, field_schema: FieldSchema) -> None:
    """Raises ValueError if field schema is marked as key and has assigned default."""
    if "default" in field_schema and field_schema.get("key"):
        raise ValueError(f"Wrong {field_name} field schema. Key can not have default value.")


def key_optionality_validator(field_name: str, field_schema: FieldSchema) -> None:
    """Raises ValueError if field schema is marked as key and optional at the same time."""
    if field_schema.get("key") and field_schema.get("optional"):
        raise ValueError(f"Wrong {field_name} field schema. Key can not be optional.")
