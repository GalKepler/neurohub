"""
Definition of the :class:`NIfTI` model.
"""
import json
from collections.abc import Iterable
from pathlib import Path

import nibabel as nib
from bids.layout import parse_file_entities
from django.db import models
from django_extensions.db.models import TimeStampedModel

# from neurohub.base_models


class NIfTI(TimeStampedModel):
    """
    A model representing a NIfTI_ file in the database.

    .. _NIfTI: https://nifti.nimh.nih.gov/nifti-1/
    """

    #: Path of the *.nii* file within the application's media directory.
    path = models.FilePathField(max_length=1000, unique=True)
    #: Associated :class:`~neurohub.base_models.models.nifti.NIfTI` instance
    parent = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        related_name="nifti_derivatives_set",
    )

    #: Whether the created instance is the product of a direct conversion from
    #: some raw format to NIfTI or of a manipulation of the data.
    is_raw = models.BooleanField(default=False)

    APPENDIX_FILES: Iterable[str] = {".json", ".bval", ".bvec"}
    B0_THRESHOLD: int = 10

    _instance: nib.nifti1.Nifti1Image = None

    # Used to cache JSON data to prevent multiple reads.
    _json_data = None

    class Meta:
        verbose_name = "NIfTI"
        ordering = ("-id",)

    def get_instance(self) -> nib.nifti1.Nifti1Image:
        """
        Returns
        -------
        nib.nifti1.Nifti1Image
            NiBabel_ instance of the NIfTI file.

        .. _NiBabel: https://nipy.org/nibabel/
        """
        return nib.load(str(self.path))

    def get_b_value(self) -> list[int]:
        """
        Returns the degree of diffusion weighting applied (b-value_) for each
        diffusion direction. This method relies on dcm2niix_'s default
        configuration in which when diffusion-weighted images (DWI_) are
        converted, another file with the same name and a "bval" extension is
        created alongside.

        .. _b-value: https://radiopaedia.org/articles/b-values-1
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Hint
        ----
        For more information, see dcm2niix's `Diffusion Tensor Imaging`_
        section of the user guide.

        .. _Diffusion Tensor Imaging:
           https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#Diffusion_Tensor_Imaging

        See Also
        --------
        * :attr:`b_value`

        Returns
        -------
        List[int]
            b-value for each diffusion direction.
        """
        file_name = self.b_value_file
        if file_name:
            with open(file_name) as file_object:
                content = file_object.read()
            content = content.splitlines()[0].split(" ")
            return [int(value) for value in content if value != ""]

    def get_b_vector(self) -> list[list[float]]:
        """
        Returns the b-vectors_ representing the diffusion weighting gradient
        scheme. This method relies on dcm2niix_'s default configuration in
        which when diffusion-weighted images (DWI_) are converted, another file
        with the same name and a "bvec" extension is created alongside.

        .. _b-vectors:
           https://mrtrix.readthedocs.io/en/latest/concepts/dw_scheme.html
        .. _dcm2niix: https://github.com/rordenlab/dcm2niix
        .. _DWI: https://en.wikipedia.org/wiki/Diffusion_MRI

        Hint
        ----
        For more information, see dcm2niix's `Diffusion Tensor Imaging`_
        section of the user guide.

        .. _Diffusion Tensor Imaging:
           https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#Diffusion_Tensor_Imaging

        See Also
        --------
        * :attr:`b_vector`

        Returns
        -------
        List[List[float]]
            b-value for each diffusion direction
        """
        file_name = self.b_vector_file
        if file_name:
            with open(file_name) as file_object:
                content = file_object.read()
            return [
                [float(value) for value in vector.rstrip().split(" ")]
                for vector in content.rstrip().split("\n")
            ]

    def read_json(self) -> dict:
        """
        Returns the JSON data generated alognside *.nii* files generated
        using dcm2niix_\'s *"BIDS sidecar"* option.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Notes
        -----
        * For more information about dcm2niix and the BIDS sidecar, see
          dcm2niix's `general usage manual`_.
        * For more information about the extracted properties and their usage
          see `Acquiring and Using Field-maps`_

        .. _Acquiring and Using Field-maps:
           https://lcni.uoregon.edu/kb-articles/kb-0003
        .. _general usage manual:
            https://www.nitrc.org/plugins/mwiki/index.php/dcm2nii:MainPage#General_Usage

        Returns
        -------
        dict
            BIDS sidecar information stored in a JSON file, or *{}* if the file
            doesn't exist
        """
        if self.json_file.is_file():
            with open(self.json_file) as f:
                return json.load(f)
        return {}

    def get_total_readout_time(self) -> float:
        """
        Reads the total readout time extracted by dcm2niix_ upon conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Hint
        ----
        Total readout time is defined as the time from the center of the first
        echo to the center of the last (in seconds).

        Returns
        -------
        float
            Total readout time
        """
        return self.json_data.get("TotalReadoutTime")

    def get_effective_spacing(self) -> float:
        """
        Reads the effective echo spacing value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        float
            Effective echo spacing
        """
        return self.json_data.get("EffectiveEchoSpacing")

    def get_phase_encoding_direction(self) -> float:
        """
        Reads the phase encoding direction value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        float
            Phase encoding direction
        """
        return self.json_data.get("PhaseEncodingDirection")

    def get_institution(self) -> str:
        """
        Reads the institution value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        str
            Institution
        """
        return self.json_data.get("InstitutionName")

    def get_file_paths(self) -> list[Path]:
        """
        Returns the list of files that are associated with the current file.

        Returns
        -------
        List[Path]
            List of associated files
        """
        nii_path = Path(self.path)
        files = [nii_path]
        base_path = nii_path.parent / nii_path.name.split(".")[0]
        for appendix in self.APPENDIX_FILES:
            appendix_path = base_path.with_suffix(appendix)
            if appendix_path.exists():
                files.append(appendix_path)
        return files

    def get_bids_entities(self) -> dict:
        """
        Returns the BIDS entities extracted from the file name.

        Returns
        -------
        dict
            BIDS entities
        """
        return parse_file_entities(self.path)

    def get_resolution(self) -> list[float]:
        """
        Returns the resolution of the image.

        Returns
        -------
        List[float]
            Resolution of the image
        """
        return self.instance.shape

    @property
    def json_file(self) -> Path:
        """
        Return path to the corresponding json file.
        Returns
        -------
        Path
            Corresponding json file
        """
        base_name = Path(self.path).name.split(".")[0]
        return (Path(self.path).parent / base_name).with_suffix(".json")

    @property
    def json_data(self) -> dict:
        """
        Reads BIDS sidecar information and caches within a local variable to
        prevent multiple reads.

        See Also
        --------
        * :meth:`read_json`

        Returns
        -------
        dict
            "BIDS sidecar" JSON data
        """
        if self._json_data is None:
            self._json_data = self.read_json()
        return self._json_data

    @property
    def b_value_file(self) -> Path:
        """
        Return FSL format b-value file path

        Returns
        -------
        Path
            FSL format b-value file path
        """
        p = Path(self.path)
        bval_file = p.parent / Path(p.stem).with_suffix(".bval")
        if bval_file.is_file():
            return bval_file

    @property
    def b_vector_file(self) -> Path:
        """
        Return FSL format b-vector file path.

        Returns
        -------
        Path
            FSL format b-vector file path
        """
        p = Path(self.path)
        bvec_file = p.parent / Path(p.stem).with_suffix(".bvec")
        if bvec_file.is_file():
            return bvec_file

    @property
    def b_value(self) -> list[int]:
        """
        Returns the B-value of DWI scans as calculated by dcm2niix_.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        See Also
        --------
        * :meth:`get_b_value`

        Returns
        -------
        List[int]
            B-value
        """
        return self.get_b_value()

    @property
    def b_vector(self) -> list[list[float]]:
        """
        Returns the B-vector of DWI scans as calculated by dcm2niix_.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        See Also
        --------
        * :meth:`get_b_vector`

        Returns
        -------
        List[List[float]]
            B-vector
        """
        return self.get_b_vector()

    @property
    def is_compressed(self) -> bool:
        """
        Whether the associated *.nii* file is compressed with gzip or not.

        Returns
        -------
        bool
            Associated *.nii* file gzip compression state
        """

        return Path(self.path).suffix == ".gz"

    @property
    def instance(self) -> nib.nifti1.Nifti1Image:
        if self._instance is None:
            self._instance = self.get_instance()
        return self._instance

    @property
    def bids_entities(self) -> dict:
        """
        Returns the BIDS entities extracted from the file name.

        Returns
        -------
        dict
            BIDS entities
        """
        return self.get_bids_entities()

    @property
    def resolution(self) -> list[float]:
        """
        Returns the resolution of the image.

        Returns
        -------
        List[float]
            Resolution of the image
        """
        return self.get_resolution()

    @property
    def institution(self) -> str:
        """
        Reads the institution value extracted by dcm2niix_ upon
        conversion.

        .. _dcm2niix: https://github.com/rordenlab/dcm2niix

        Returns
        -------
        str
            Institution
        """
        return self.get_institution()
