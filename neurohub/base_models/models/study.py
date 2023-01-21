"""
Definition of the :class:`Study` model.
"""
import pandas as pd
from django.db import models
from django_extensions.db.models import TimeStampedModel, TitleDescriptionModel

from neurohub.base_models.models.session import Session
from neurohub.base_models.models.subject import Subject

STUDY_IMAGE_UPLOAD_DESTINATION: str = "images/studies"


class Study(TitleDescriptionModel, TimeStampedModel):
    """
    Represents a single study in the database.
    """

    #: An optional image associated with this study.
    image = models.ImageField(
        upload_to=STUDY_IMAGE_UPLOAD_DESTINATION, blank=True, null=True
    )
    title = models.CharField(max_length=256, unique=True)
    groups = models.ManyToManyField("base_models.Group", blank=True)
    conditions = models.ManyToManyField("base_models.Condition", blank=True)

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
        verbose_name_plural = "studies"

    def query_associated_subjects(self):
        """
        Returns
        -------
        QuerySet
            QuerySet of associated subjects
        """
        return Subject.objects.filter(
            condition__in=self.conditions.all(), group__in=self.groups.all()
        )

    def query_associated_sessions(self):
        """
        Returns
        -------
        QuerySet
            QuerySet of associated sessions
        """
        return Session.objects.filter(
            condition__in=self.conditions.all(), group__in=self.groups.all()
        )

    def generate_subjects_table(self):
        """
        Returns
        -------
        pandas.DataFrame
            DataFrame of associated subjects
        """
        subjects = self.query_associated_subjects()
        return pd.DataFrame(
            [
                {
                    "id": subject.pk,
                    "study": self.title,
                    "group": [
                        g for g in subject.group_set.all() if g in self.groups.all()
                    ][0],
                    "condition": [
                        c
                        for c in subject.condition_set.all()
                        if c in self.conditions.all()
                    ][0],
                }
                for subject in subjects
            ]
        )

    def generate_full_subjects_table(self):
        """
        Returns
        -------
        pandas.DataFrame
            DataFrame of associated subjects
        """
        subjects = self.query_associated_subjects()
        df = pd.DataFrame()
        for subject in subjects:
            questionnaire_data = subject.get_questionnaire_data().copy()
            questionnaire_data["pylabber_id"] = subject.pk
            questionnaire_data["study"] = self.title
            questionnaire_data["group"] = [
                g for g in subject.group_set.all() if g in self.groups.all()
            ][0]
            questionnaire_data["condition"] = [
                c for c in subject.condition_set.all() if c in self.conditions.all()
            ][0]
            df = pd.concat([df, questionnaire_data], axis=0)
        return df.reset_index(drop=True)
