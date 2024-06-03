from typing import Type, get_origin, Union, get_args


def _is_optional(field_type: Type) -> bool:
    """
    According to https://stackoverflow.com/questions/56832881/check-if-a-field-is-typing-optional
    this checks if field is Optional
    :param field_type: type of the field
    :returns: true if field is Optional
    """
    return get_origin(field_type) is Union and type(None) in get_args(field_type)
