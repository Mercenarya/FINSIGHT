from __future__ import annotations

from django.db.models import F, Manager, QuerySet

from django_utils.models.lookup import TupleAnnotation


class CustomDjangoQuerySet(QuerySet):
    """
    Custom queryset for django models.
    """

    def filter_tuple(self, *, fields, values) -> CustomDjangoQuerySet:
        """
        Filters the QuerySet based on a combination of fields using tuple values.

        This method allows filtering the QuerySet by specifying a combination of
        fields that must match any of the provided tuples in `values`. It leverages
        Django's annotation and custom lookup to perform the tuple filtering.

        Args:
            fields (list of str): A list of field names to filter on. Each field
                in the list corresponds to a part of the tuple being filtered.
                For example, ['field1', 'field2'] will filter based on the
                combination of `field1` and `field2`.
            values (list of tuple): A list of tuples containing the values to filter by.
                Each tuple should have values corresponding to the `fields`.
                For example, [(value1_1, value1_2), (value2_1, value2_2)].

        Returns:
            CustomDjangoQuerySet: The filtered QuerySet with the specified tuple filter applied.

        Example:
            queryset = MyModel.objects.filter_tuple(
                fields=['user_id', 'learning_item_id'],
                values=[(2, 1), (3, 2)]
            )
        SQL:
            SELECT *
            FROM mymodel
            WHERE (user_id, learning_item_id) IN ((2, 1), (3, 2));
        """
        return self.alias(
            tuple_field=TupleAnnotation(*[F(field) for field in fields])
        ).filter(tuple_field__tuple_in=values)


class CustomDjangoManager(Manager):
    """
    Custom manager for django models.
    """

    def get_queryset(self) -> CustomDjangoQuerySet:
        return CustomDjangoQuerySet(self.model, using=self._db)

    def filter_tuple(self, *, fields, values) -> CustomDjangoQuerySet:
        return self.get_queryset().filter_tuple(fields=fields, values=values)
