from django.db import models


class BaseModel(models.Model):
    """
    Abstract base model providing automatic timestamp fields.
    All app models should inherit from this instead of repeating timestamps.
    """

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
