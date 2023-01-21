from datetime import date

STUDIES = {
    "TheBase": {
        "possible_titles": ["the base"],
        "description": "Scanning the general population",
        "groups": ["General Population"],
        "derive_study_from": "Study",
    },
    "NFS": {
        "possible_titles": ["nfs"],
        "description": "Need For Speed study",
        "groups": ["Short", "Long", "Active", "Passive"],
        "conditions": ["Learners", "Controls"],
        "derive_study_from": "Study",
        "start_date": date(2008, 9, 1),
        "end_date": date(2016, 5, 1),
    },
    "Sports": {
        "possible_titles": ["sport"],
        "description": "Sports study",
        "groups": ["Climbing", "BJJ"],
        "conditions": ["Learners", "Controls", "Experts"],
        "derive_study_from": "Study",
        "start_date": date(2020, 10, 1),
    },
    "Music": {
        "possible_titles": ["music"],
        "description": "Music study",
        "groups": ["Trumpet"],
        "conditions": ["Learners", "Controls", "Experts"],
        "derive_study_from": "Group",
        "start_date": date(2022, 1, 1),
    },
    "Python": {
        "possible_titles": ["python"],
        "description": "Python programming study",
        "groups": ["python"],
        "conditions": ["Learners", "Controls"],
        "derive_study_from": "Group",
        "start_date": date(2021, 1, 1),
    },
}
