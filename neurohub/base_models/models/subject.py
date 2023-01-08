"""
Definition of the :class:`Subject` model.
"""

from datetime import date
from typing import Any

import pandas as pd
from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from django_extensions.db.models import TimeStampedModel
from questionnaire_reader import QuestionnaireReader

from neurohub.base_models.utils import read_pylabber_table, read_subject_table


class Subject(TimeStampedModel):
    """
    Represents a single research subject. Any associated data model should be
    associated with this model.
    """

    PYLABBER_COLUMNS_MAPPER = {
        "id_number": "ID Number",
        "first_name": "First Name",
        "last_name": "Last Name",
        "date_of_birth": "Date Of Birth",
        "sex": "Sex",
        "dominant_hand": "Dominant Hand",
    }
    CRF_COLUMNS_MAPPER = {
        "questionnaire_id": "Questionnaire",
    }
    #: Some representative ID number unique to this subject.
    pylabber_id = models.IntegerField(primary_key=True)

    #: Subject's ID number.
    id_number = models.CharField(max_length=64, blank=True, null=True)

    #: Subject's first name.
    first_name = models.CharField(max_length=64, blank=True, null=True)

    #: Subject's last name.
    last_name = models.CharField(max_length=64, blank=True, null=True)

    #: Subject's date of birth.
    date_of_birth = models.DateField(
        verbose_name="Date of Birth",
        blank=True,
        null=True,
        validators=[MaxValueValidator(date.today())],
    )

    #: Custom attributes dictionary.
    custom_attributes = models.JSONField(blank=True, default=dict)

    BIDS_DIR_TEMPLATE: str = "sub-{pylabber_id}"

    class Meta:
        ordering = ("-pylabber_id",)

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._bids_dir = None

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.

        Returns
        -------
        str
            String representation
        """
        return f"Subject #{self.pylabber_id}"

    def get_full_name(self) -> str:
        """
        Returns a formatted string with the subject's full name (first name
        and then last name).

        Returns
        -------
        str
            Subject's full name
        """
        return f"{self.first_name} {self.last_name}"

    def get_crf_information(self) -> pd.Series:
        """
        Temporary method to use an external table to retrieve subject
        personal information.

        Returns
        -------
        pd.Series
            Subject personal information
        """
        subject_table = read_subject_table()
        subject_table["Questionnaire"].fillna("", inplace=True)
        this_subject = subject_table["ID"] == self.id_number
        return subject_table[this_subject].drop_duplicates(subset="ID", keep="last")

    def get_pylabber_information(self) -> pd.Series:
        """
        Temporary method to use an external table to retrieve subject
        personal information.

        Returns
        -------
        pd.Series
            Subject personal information
        """
        subject_table = read_pylabber_table()
        this_subject = subject_table["ID"] == self.pylabber_id
        return subject_table[this_subject].drop_duplicates(
            subset="ID Number", keep="last"
        )

    def update_subject_from_pylabber(self):
        """
        Temporary method to use an external table to retrieve subject
        personal information.
        """
        this_subject = self.get_pylabber_information()
        for key, value in self.PYLABBER_COLUMNS_MAPPER.items():
            setattr(self, key, this_subject[value].squeeze())
        self.save()

    def update_subject_from_crf(self):
        """
        Temporary method to use an external table to retrieve subject
        personal information.
        """
        this_subject = self.get_crf_information()
        for key, value in self.CRF_COLUMNS_MAPPER.items():
            setattr(self, key, this_subject[value].squeeze())
        self.save()

    def get_questionnaire_data(self):
        """
        A method to link between a subject to it's questionnaire data.

        Returns
        -------
        pd.Series
            Subject and Questionnaire information.
        """
        # Getting the questionnaire data from the sheets document.
        questionnaire = QuestionnaireReader(path=settings.QUESTIONNAIRE_PATH).data
        questionnaire["Timestamp"] = questionnaire["Timestamp"].astype(str)
        # Getting the subject's questionnaire data.
        this_subject = questionnaire["Subject ID"] == self.questionnaire_id
        return questionnaire[this_subject].drop_duplicates(
            subset=["Subject ID"], keep="last"
        )

    @property
    def crf_information(self) -> pd.DataFrame:
        """
        Temporary method to use an external table to retrieve subject
        personal information.

        Returns
        -------
        pd.DataFrame
            Subject personal information
        """
        return self.get_crf_information()

    @property
    def pylabber_information(self) -> pd.DataFrame:
        """
        Temporary method to use an external table to retrieve subject
        personal information.

        Returns
        -------
        pd.DataFrame
            Subject personal information
        """
        return self.get_pylabber_information()

    @property
    def questionnaire_data(self) -> pd.DataFrame:
        """
        A method to link between a subject to it's questionnaire data.

        Returns
        -------
        pd.DataFrame
            Subject and Questionnaire information.
        """
        return self.get_questionnaire_data()
