import json
from pathlib import Path

from django.db import models


class Scan(models.Model):
    """Scan model."""

    class Meta:
        """Meta class."""

        verbose_name = "Scan"
        verbose_name_plural = "Scans"

    nifti_path = models.CharField(max_length=255)
    json_path = models.CharField(max_length=255, null=True)

    def get_path_name(self):
        """Return the name of the NIfTI file."""
        return Path(self.nifti_path).name

    def __str__(self):
        """Return the name of the scan."""
        return self.get_path_name()

    def read_json(self):
        """Read the JSON file."""

        with open(self.json_path) as f:
            return json.load(f)
