"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Literal
from rockeet.helper import Response, endpoint, isFileId


def allEntites(assistantId: str, expand: list[Literal["examples", "autoExtend", "useSynonyms", "strictness", "metadata"]]=[], **kwargs) -> Response:
    """List an entities of an assistant"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(expand, list), "expand parameter must be a list"

    return endpoint("/assistant/entities", {
        **kwargs,
        "assistantId": assistantId,
        "expand": expand,
    }, method="get")
