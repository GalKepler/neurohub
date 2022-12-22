import json
from pathlib import Path

import nibabel as nib
from django.db import models

DIMENSIONS_TO_AXES = {0: "x", 1: "y", 2: "z", 3: "t"}


class Scan(models.Model):
    """Scan model."""

    class Meta:
        """Meta class."""

        verbose_name = "Scan"
        verbose_name_plural = "Scans"

    nifti_path = models.CharField(max_length=255)
    json_path = models.CharField(max_length=255, null=True)
    related_scans = models.ManyToManyField("self")

    def __init__(self, *args, **kwargs):
        """Initialize the Scan object."""
        super().__init__(*args, **kwargs)
        self.parse_json_to_attributes()
        self.store_image_shape()

    def get_path_name(self):
        """Return the name of the NIfTI file."""
        return Path(self.nifti_path).name

    def __str__(self):
        """Return the name of the scan."""
        return self.get_path_name()

    def parse_json_to_attributes(self):
        """Parse the JSON file and set the attributes of the Scan object."""
        if not self.json_path:
            return
        with open(self.json_path) as json_file:
            json_data = json.load(json_file)
            for key, value in json_data.items():
                setattr(self, key, value)

    def store_image_shape(self):
        """Store the shape of the image."""
        dim_info = self.nifti.header.get_dim_info()
        image_size = self.nifti.shape
        for dim in dim_info:
            setattr(self, f"dimension_{DIMENSIONS_TO_AXES[dim]}", image_size[dim])

    @property
    def id(self):
        """Return the ID of the scan."""
        return self.pk

    @property
    def nifti(self):
        """Return the NIfTI file."""
        return nib.load(self.nifti_path)
