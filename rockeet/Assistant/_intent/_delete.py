"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def deleteIntent(assistantId: str, intentName: str, **kwargs) -> Response:
    """Delete an intent"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"

    return endpoint("/assistant/intent", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
    }, method="delete")
