from types import FunctionType

from django.db import models

from django_utils.models.queryset import CustomDjangoManager


class BaseModelMeta(models.base.ModelBase):
    """
    Metaclass for all models validations.
    """

    def __new__(cls, name, bases, attrs, **kwargs):
        attrs["_clean_validations"] = {
            key
            for key, value in attrs.items()
            if key.startswith("clean_") and isinstance(value, FunctionType)
        }

        attrs["_full_clean_validations"] = {
            key
            for key, value in attrs.items()
            if key.startswith("full_clean_") and isinstance(value, FunctionType)
        }

        return super().__new__(cls, name, bases, attrs, **kwargs)


class Model(models.Model, metaclass=BaseModelMeta):
    """
    Base mode with custom save and full_clean methods.
    It also provides a custom manager that can be used to filter out
    """

    class Meta:
        abstract = True

    objects = CustomDjangoManager()

    def save(self, *args, **kwargs):
        skip_clean = kwargs.pop("skip_clean", False)
        if not skip_clean:
            self.full_clean(exclude=kwargs.pop("exclude_clean", None))
        return super().save(*args, **kwargs)

    def full_clean(self, *args, **kwargs) -> None:
        super(BaseModel, self).full_clean(*args, **kwargs)
        for validation in self._full_clean_validations:
            getattr(self, validation)()

    def clean(self) -> None:
        super(BaseModel, self).clean()
        for validation in self._clean_validations:
            getattr(self, validation)()
