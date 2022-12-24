import unittest
from pathlib import Path

from neurohub.base_models.models.nifti import NIfTI  # noqa: F401


class TestNifti(unittest.TestCase):
    TEST_BIDS_DIR = "neurohub/base_models/tests/data/bids_dataset"
    NIFTIS = {
        "anat": "sub-2321/ses-202202131331/anat/sub-2321_ses-202202131331_ce-corrected_T1w.nii.gz",
        "dwi": "sub-2321/ses-202202131331/dwi/sub-2321_ses-202202131331_dir-FWD_dwi.nii.gz",
    }

    def setUp(self):
        pass

    def test_nifti(self):
        nifti = NIfTI()
        assert nifti is not None

    def test_anat_nifti(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["anat"])
        assert nifti is not None

    def test_anat_json(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["anat"])
        assert nifti.json_file is not None

    def test_dwi_nifti(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["dwi"])
        assert nifti is not None

    def test_dwi_json(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["dwi"])
        assert nifti.json_file is not None

    def test_dwi_bval(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["dwi"])
        assert nifti.b_value_file is not None

    def test_dwi_bvector(self):
        nifti = NIfTI(path=Path(self.TEST_BIDS_DIR) / self.NIFTIS["dwi"])
        assert nifti.b_vector_file is not None
