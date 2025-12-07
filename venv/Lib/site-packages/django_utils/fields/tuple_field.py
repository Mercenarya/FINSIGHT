"""
This file has all custom model fields
"""

import ast

from django.db.models import Field as BaseField


class TupleField(BaseField):
    """
    This field is used to handle output for custom TupleAnnotation function.
    """

    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return ast.literal_eval(value)
