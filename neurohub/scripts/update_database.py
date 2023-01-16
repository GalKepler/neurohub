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
    paths = len(list(base_dir.rglob(pattern)))
    with tqdm.tqdm(total=paths) as pbar:
        for path in base_dir.rglob(pattern):
            tensor, created = TensorDerivative.objects.get_or_create(path=path)
            tensor.software_used = tensor.get_estimator()
            tensor.set_bids_entities_as_properties()
            if created and tensor.is_unique_derivative():
                tensor.save()
                session_id = tensor.bids_entities.get("session")
                subject_id = tensor.bids_entities.get("subject")
                subject, _ = Subject.objects.get_or_create(pylabber_id=subject_id)
                session, _ = Session.objects.get_or_create(bids_dir=session_id)
                session.subject = subject
                session.save()
            pbar.update(1)


def associate_sessions_to_studies() -> None:
    """
    Associates sessions to studies.
    """
    for session in Session.objects.all():
        session.study = session.subject.study
        session.save()
