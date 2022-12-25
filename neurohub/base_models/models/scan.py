from django.db import models

from neurohub.base_models.models.nifti import NIfTI
from neurohub.base_models.models.tensor_derivative import TensorDerivative


class Scan(models.Model):
    """Scan model."""

    class Meta:
        """Meta class."""

        verbose_name = "Scan"
        verbose_name_plural = "Scans"

    nifti = models.OneToOneField(
        NIfTI, on_delete=models.CASCADE, null=True
    )  # associated NIfTI file
    tensor_derivatives = models.ManyToManyField(
        TensorDerivative
    )  # associated tensor derivatives
    related_scans = models.ManyToManyField("self")  # related scans
