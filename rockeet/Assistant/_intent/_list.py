"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Literal
from rockeet.helper import Response, endpoint, isFileId


def allIntents(assistantId: str, expand: list[Literal["utterances", "slots", "metadata"]]=[], **kwargs) -> Response:
    """List an intents of an assistant"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(expand, list), "expand parameter must be a list"

    return endpoint("/assistant/intents", {
        **kwargs,
        "assistantId": assistantId,
        "expand": expand,
    }, method="get")
