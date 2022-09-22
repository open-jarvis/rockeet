"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Literal
from rockeet.helper import Response, endpoint, isFileId


def getIntent(assistantId: str, intentName: str, expand: list[Literal["utterances", "slots", "metadata"]] = ["utterances", "slots"], **kwargs) -> Response:
    """List an intents of an assistant"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a str"
    assert isinstance(expand, list), "expand parameter must be a list"

    return endpoint("/assistant/intent", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "expand": ",".join(expand),
    }, method="get")
