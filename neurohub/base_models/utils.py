import pandas as pd
from django.conf import settings


def convert_id_to_str(value: float) -> str:
    return str(int(value)).zfill(9) if not pd.isna(value) else value


def read_subject_table() -> pd.DataFrame:
    """
    Temporary method to use an external table to retrieve subject

    Returns
    -------
    pd.DataFrame
        Subjects information from the CRF
    """
    return pd.read_excel(
        settings.CRF_TABLE_PATH,
        sheet_name="גיליון1",
        header=0,
        converters={
            "ID": convert_id_to_str,
            "Questionnaire": str,
        },
    )


def read_pylabber_table() -> pd.DataFrame:
    """
    Temporary method to use an external table to retrieve subject

    Returns
    -------
    pd.DataFrame
        Subjects information from pylabbaer
    """
    return pd.read_csv(
        settings.PYLABBER_TABLE_PATH,
    )


def merge_subject_and_questionnaire_data(
    subject_data, questionnaire_data
) -> pd.DataFrame:
    return pd.merge(
        subject_data,
        questionnaire_data,
        how="inner",
        left_on=subject_data["Questionnaire", "Questionnaire"],
        right_on=questionnaire_data.index,
    )
