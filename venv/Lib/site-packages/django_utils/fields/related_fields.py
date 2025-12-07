from collections import defaultdict

from django.core.exceptions import MultipleObjectsReturned
from django.db import models
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor


class CustomDescriptor(ForwardManyToOneDescriptor):
    """
    Custom Accessor to the related object on the forward side of a many-to-one or
    one-to-one (via ForwardOneToOneDescriptor subclass) relation.
    """

    def get_object(self, instance):
        qs = self.get_queryset(instance=instance)
        try:
            return qs.get(self.field.get_reverse_related_filter(instance))
        except MultipleObjectsReturned:
            return qs.filter(self.field.get_reverse_related_filter(instance))


class RelatedField(models.ForeignObject):
    """
    Create a django link between models on a field where a foreign key isn't used.
    This class allows that link to be realised through a proper relationship,
    allowing prefetches and select_related.
    """

    def get_cache_name(self):
        return self.name

    def __init__(self, model, from_fields, to_fields, **kwargs):
        self.forward_related_accessor_class = CustomDescriptor
        super().__init__(
            model,
            on_delete=models.DO_NOTHING,
            from_fields=from_fields,
            to_fields=to_fields,
            null=True,
            blank=True,
            **kwargs,
        )

    def contribute_to_class(
        self,
        cls,
        name,
        private_only=True,
        related_field=defaultdict(list),
        **kwargs,
    ):
        # override the default to always make it private
        # this ensures that no additional columns are created
        super().contribute_to_class(cls, name, private_only=private_only, **kwargs)
        related_field[cls].append(name)

        def get_deferred_fields(self):
            deferred_fields = super(  # pylint: disable=bad-super-call
                cls, self
            ).get_deferred_fields()
            deferred_fields.update(related_field[cls])
            return deferred_fields

        setattr(cls, "get_deferred_fields", get_deferred_fields)
