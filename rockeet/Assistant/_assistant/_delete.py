"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def deleteAssistant(assistantId: str, **kwargs) -> Response:
    """Delete an entity"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"

    return endpoint("/assistant", {
        **kwargs,
        "assistantId": assistantId,
    }, method="delete")
