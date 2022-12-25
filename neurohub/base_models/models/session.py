"""
Definition of the :class:`Session` class.
"""
from datetime import datetime
from pathlib import Path

from django.db import models
from django.db.models.query import QuerySet
from django_extensions.db.models import TimeStampedModel

from neurohub.base_models.models.tensor_derivative import TensorDerivative

SECONDS_IN_YEAR: int = 60 * 60 * 24 * 365
CLAIMED_SESSION_STRING: str = "Subject #{subject_id} MRI session from {date}"
UNCLAIMED_SESSION_STRING: str = "Unclaimed MRI session from {date}"
NIFTI_FILES_KEY: str = "_nifti__path"


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: The date and time in which this scanning sequence began.
    _time = models.DateTimeField(null=True)

    BIDS_DIR_TEMPLATE: str = "ses-{date}{time}"
    SESSION_DATE_FORMAT: str = "%Y%m%d"
    SESSION_TIME_FORMAT: str = "%H%M"

    def __str__(self) -> str:
        """
        Returns the string representation of this instance.
        Returns
        -------
        str
            String representation
        """
        date = self.time.date()
        if hasattr(self, "subject"):
            return CLAIMED_SESSION_STRING.format(subject_id=self.subject.id, date=date)
        return UNCLAIMED_SESSION_STRING.format(date=date)

    def infer_time_from_nifti(self) -> None:
        """
        Infers the time of the session from the time of the first NIfTI file.
        """
        nifti = self.nifti_set.first()
        if nifti and not self._time:
            time_str = nifti.bids_entities.get("session")
            self._time = datetime.strptime(
                time_str, self.SESSION_DATE_FORMAT + self.SESSION_TIME_FORMAT
            )

    def list_nifti_files(self) -> list[Path]:
        """
        Returns a list of *.nii* files (and by default also JSON sidecars)
        included in this session.
        Returns
        -------
        List[Path]
            *.nii* files
        """
        paths = []
        for nifti in self.nifti_set.all():
            nii_paths = nifti.get_file_paths()
            paths += nii_paths
        return paths

    def list_derivatives(self) -> QuerySet:
        """
        Returns a list of tensor derivatives included in this session.

        Returns
        -------
        List[TensorDerivative]
            Tensor derivatives
        """
        return TensorDerivative.objects.filter(parent__in=self.nifti_set.all())

    @property
    def derivatives_set(self) -> QuerySet:
        """
        Returns a list of tensor derivatives included in this session.
        Returns
        -------
        List[TensorDerivative]
            Tensor derivatives
        """
        return self.list_derivatives()

    @property
    def nifti_files(self) -> list[Path]:
        """
        Returns a list of *.nii* files (and by default also JSON sidecars)
        included in this session.
        Returns
        -------
        List[Path]
            *.nii* files
        """
        return self.list_nifti_files()

    @property
    def time(self) -> datetime:
        """
        Returns the time of the session.
        Returns
        -------
        datetime
            Time of the session
        """
        if not self._time:
            self.infer_time_from_nifti()
        return self._time
