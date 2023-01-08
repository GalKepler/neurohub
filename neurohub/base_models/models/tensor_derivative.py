from pathlib import Path

import pandas as pd
from bids.layout import parse_file_entities
from django.db import models
from django_extensions.db.models import TimeStampedModel

TENSOR_ESTIMATORS = ["dipy", "mrtrix3", "fsl"]
MATCHING_ENTITIES = ["subject", "session"]


class TensorDerivative(TimeStampedModel):
    """
    A model representing a tensor-based derivative,
    which is a pickle storing a dataframe describing different
    tensor-derived metrics for a given scan and parcellation atlas.
    """

    # path to the pickle file
    path = models.FilePathField(max_length=1000, unique=True)

    # the scan this derivative is associated with
    nifti_parent = models.ForeignKey(
        "base_models.NIfTI",
        on_delete=models.CASCADE,
        null=True,
        related_name="tensor_derivatives_set",
    )
    session = models.ForeignKey(
        "base_models.Session",
        on_delete=models.CASCADE,
        null=True,
        related_name="tensor_derivatives_set",
        unique=True,
    )

    #: BIDS entities for easy access
    software_used = models.CharField(max_length=100, null=True)
    acquisition = models.CharField(max_length=100, null=True)
    atlas = models.CharField(max_length=100, null=True)
    label = models.CharField(max_length=100, null=True)

    def validate_same_bids_entities(self):
        """
        Check that the parent scan and the derivative are from the same subject.
        """
        for entity in MATCHING_ENTITIES:
            if self.parent.bids_entities.get(entity) != self.bids_entities.get(entity):
                raise ValueError(
                    f"The parent scan and the derivative are not from the same {entity}."
                )

    def get_dataframe(self):
        """
        Return the dataframe stored in the pickle file.
        """
        return pd.read_pickle(self.path)

    def get_bids_entities(self):
        """
        Return the BIDS entities of the parent scan.
        """
        return parse_file_entities(self.path)

    def set_bids_entities_as_properties(self):
        """
        Set the BIDS entities of the parent scan as properties.
        """
        for entity, value in self.bids_entities.items():
            setattr(self, entity, value)

    def get_estimator(self):
        """
        Return the estimator used to produce this derivative.
        """
        derivative_path = Path(self.path)
        estimator = derivative_path.parent.name
        return estimator if estimator in TENSOR_ESTIMATORS else None

    @property
    def data(self):
        """
        Return the dataframe stored in the pickle file.
        """
        return self.get_dataframe()

    @property
    def bids_entities(self):
        """
        Return the BIDS entities of the parent scan.
        """
        return self.get_bids_entities()

    @property
    def estimator(self):
        """
        Return the estimator used to produce this derivative.
        """
        return self.get_estimator()
