"""
Definition of the :class:`Session` class.
"""
from datetime import datetime
from pathlib import Path

from django.db import models
from django.db.models.query import QuerySet
from django_extensions.db.models import TimeStampedModel
from meteostat import Hourly, Point

from neurohub.base_models.models.tensor_derivative import TensorDerivative

SECONDS_IN_YEAR: int = 60 * 60 * 24 * 365
CLAIMED_SESSION_STRING: str = "Subject #{subject_id} MRI session from {date}"
UNCLAIMED_SESSION_STRING: str = "Unclaimed MRI session from {date}"
NIFTI_FILES_KEY: str = "_nifti__path"


class Session(TimeStampedModel):
    """
    Represents a single MRI scanning session.
    """

    #: BIDS format directory name.
    bids_dir = models.CharField(max_length=255, unique=True)

    #: The time of the session.
    time = models.DateTimeField(null=True)

    #: The subject this session belongs to.
    subject = models.ForeignKey(
        "base_models.Subject",
        on_delete=models.CASCADE,
        null=True,
        related_name="session_set",
    )

    #: BIDS format directory name.
    BIDS_DIR_TEMPLATE: str = "ses-{date}{time}"

    #: BIDS format session date format.
    SESSION_DATE_FORMAT: str = "%Y%m%d"
    SESSION_TIME_FORMAT: str = "%H%M"

    #: Location of the scanning session.
    LOCATION = {"lon": 34.8, "lat": 32.0833}  # Tel Aviv
    POINT = Point(**LOCATION)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.time:
            self.infer_time()

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
            return CLAIMED_SESSION_STRING.format(
                subject_id=self.subject.pylabber_id, date=date
            )
        return UNCLAIMED_SESSION_STRING.format(date=date)

    def infer_time(self) -> None:
        """
        Infers the time of the session from the BIDS directory name.
        """
        time_str = self.bids_dir.split("-")[-1]
        self.time = datetime.strptime(
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

    def get_weather_data(self) -> dict:
        """
        Returns the weather data for the session location.
        Returns
        -------
        pd.DataFrame
            `Hourly weather data`_
            .. _Hourly weather data: https://dev.meteostat.net/api/point/hourly.html
        """
        day_start = self.time.replace(hour=0, minute=0, second=0)
        day_end = self.time.replace(hour=23, minute=59, second=59)
        weather_during_day = Hourly(self.POINT, day_start, day_end).fetch()
        closest_reading = weather_during_day.index[
            weather_during_day.index.searchsorted(self.time)
        ]
        return weather_during_day.loc[[closest_reading]]

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
    def weather_data(self) -> dict:
        """
        Returns the weather data for the session location.
        Returns
        -------
        pd.DataFrame
            `Hourly weather data`_
            .. _Hourly weather data: https://dev.meteostat.net/api/point/hourly.html
        """
        return self.get_weather_data()
