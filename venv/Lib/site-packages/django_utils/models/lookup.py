from django.db import models
from django.db.models import Func, Lookup

from django_utils.constants import LOOKUP_NOT_ALLOWED
from django_utils.fields.tuple_field import TupleField


class TupleAnnotation(Func):
    """
    An annotation class used to represent tuples in SQL expressions.

    This class generates a SQL expression representing a tuple, which can be
    used for filtering or other purposes in a Django QuerySet.

    Attributes:
        function (str): Specifies the SQL function to use, left empty since
            we're creating a tuple representation.
        template (str): The SQL template used to render the expression.
            Here, it represents a tuple with placeholders for the fields.
        output_field (Field): load data as tuple object in python from database.
    """

    function = ""
    template = "(%(expressions)s)"
    output_field = TupleField()


@models.Field.register_lookup
class TupleIn(Lookup):
    """
    A custom Django lookup class that allows filtering based on tuples.

    This lookup enables filtering QuerySets by checking if a tuple of fields
    is present within a list of tuples provided. It uses the `IN` SQL clause
    to perform the check, ensuring that the fields match one of the specified tuples.

    Attributes:
        lookup_name (str): The name of the custom lookup, which is `tuple_in`.

    Methods:
        as_sql(compiler, connection):
            Generates the SQL query and parameters for this lookup.

            Raises:
                Exception: If the left-hand side of the lookup is not an instance
                of `TupleAnnotation`, indicating the lookup is not allowed.
    """

    lookup_name = "tuple_in"

    def as_sql(self, compiler, connection):
        if not isinstance(self.lhs, TupleAnnotation):
            raise Exception(LOOKUP_NOT_ALLOWED.format(obj_class=self.lhs.__class__))
        lhs, lhs_params = self.process_lhs(compiler, connection)
        rhs, rhs_params = self.process_rhs(compiler, connection)
        rhs_tuples = rhs_params[0]

        # Generate a single placeholder string with the correct number of %s
        placeholder_template = f"({', '.join(['%s'] * len(rhs_tuples[0]))})"
        placeholders = ", ".join([placeholder_template] * len(rhs_tuples))

        # Flatten the tuples for the SQL parameters
        params = lhs_params + [item for tup in rhs_tuples for item in tup]

        return f"{lhs} IN ({placeholders})", params
