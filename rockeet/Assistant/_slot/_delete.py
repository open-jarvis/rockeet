"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def deleteSlot(assistantId: str, intentName: str, slotName: str, **kwargs) -> Response:
    """Delete a slot from an intent"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"
    assert isinstance(slotName, str), "slotName parameter must be a string"

    return endpoint("/assistant/intent/slot", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "slotName": slotName,
    }, method="delete")
