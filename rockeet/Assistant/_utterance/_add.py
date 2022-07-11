"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet.helper import Response, endpoint, isFileId


def addUtterance(assistantId: str, intentName: str, utterance: Union[list,str], index: int = None, **kwargs) -> Response:
    """Add an utterance to an intent"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"
    assert isinstance(utterance, list) or isinstance(utterance, str), "utterance parameter must be either list or string"
    assert isinstance(utterance, int) or index is None, "index parameter must be integer or None"

    body = {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "utterance": utterance
    }

    if index is not None:
        body["index"] = index

    return endpoint("/assistant/intent/utterance", body, method="put")
