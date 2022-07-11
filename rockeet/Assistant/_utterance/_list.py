"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet.helper import Response, endpoint, isFileId


def allUtterances(assistantId: str, intentName: str, **kwargs) -> Response:
    """Add an utterance to an intent"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"

    body = {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
    }

    return endpoint("/assistant/intent/utterances", body, method="get")
