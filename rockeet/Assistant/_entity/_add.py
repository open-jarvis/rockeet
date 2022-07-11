"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def addEntity(assistantId: str, name: str, examples: list, autoExtend: bool = True, useSynonyms: bool = True, strictness: float = 0.8, metadata: dict = {}) -> Response:
    """Add an entity to an assistant
    """

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(name, str), "name parameter must be a string"
    assert isinstance(examples, list) and len(examples) > 0, "examples parameter must be a list with at least one element"
    assert isinstance(autoExtend, bool), "autoExtend parameter must be a boolean"
    assert isinstance(useSynonyms, bool), "useSynonyms parameter must be a boolean"
    assert isinstance(strictness, float) and 0 <= strictness <= 1, "strictness parameter must be a float between 0 and 1"
    assert isinstance(metadata, dict), "metadata parameter must be a dictionary"

    return endpoint("/assistant/entity", {
        "assistantId": assistantId,
        "name": name,
        "examples": examples,
        "autoExtend": autoExtend,
        "useSynonyms": useSynonyms,
        "strictness": strictness,
        "metadata": metadata,
    })
