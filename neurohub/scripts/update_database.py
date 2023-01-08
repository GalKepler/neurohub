from pathlib import Path

import tqdm

from neurohub.base_models.models import Session, Subject, TensorDerivative


def collect_tensor_derivatives(
    base_dir: Path, pattern: str = "sub-*_dseg.pickle"
) -> None:
    """
    Collects tensor derivatives from a base directory.

    Parameters
    ----------
    base_dir : Path
        Base directory
    pattern : str, optional
        Glob pattern, by default "sub-*_dseg.pickle"
    """
    for path in tqdm.tqdm(base_dir.rglob(pattern)):
        tensor, created = TensorDerivative.objects.get_or_create(path=path)
        tensor.software_used = tensor.get_estimator()
        tensor.set_bids_entities_as_properties()
        tensor.save()
        if created:
            session_id = tensor.bids_entities.get("session")
            subject_id = tensor.bids_entities.get("subject")
            subject, _ = Subject.objects.get_or_create(pylabber_id=subject_id)
            session, _ = Session.objects.get_or_create(bids_dir=session_id)
            session.subject = subject
            session.save()
