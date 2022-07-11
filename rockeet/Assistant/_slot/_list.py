"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Literal
from rockeet.helper import Response, endpoint, isFileId


def allSlots(assistantId: str, intentName: str, expand: bool = True, **kwargs) -> Response:
    """Get a list of all slots associated with an intent"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"
    assert isinstance(expand, bool), "expand parameter must be a list"

    return endpoint("/assistant/intent/slots", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "expand": expand,
    }, method="get")
