"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def deleteUtterance(assistantId: str, intentName: str, index: int, **kwargs) -> Response:
    """Delete an utterance"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"
    assert isinstance(index, int) and index >= 0, "index parameter must be an index and greater than or equal to 0"

    return endpoint("/assistant/intent/utterance", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "index": index
    }, method="delete")
