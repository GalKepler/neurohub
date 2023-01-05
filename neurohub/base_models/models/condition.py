"""
Definition of the :class:`Study` model.
"""
from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel


class Condition(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a single study in the database.
    """

    #: Subjects associated with this condition.
    #: This field is currently not used, but kept because in the future it
    #: might be used for "caching" associated subjects to save queries.
    subjects = models.ManyToManyField("base_models.Subject", blank=True)

    def __str__(self):
        """
        Returns
        -------
        str
            String representation
        """
        return self.title

    class Meta:
        ordering = ["title"]
        verbose_name_plural = "conditions"
