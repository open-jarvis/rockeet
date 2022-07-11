"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def train(assistantId: str) -> Response:
    """Train an assistant
    """

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"

    return endpoint("/assistant/train", {
        "assistantId": assistantId,
    })
