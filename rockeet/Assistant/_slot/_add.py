"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def addSlot(assistantId: str, intentName: str, slotName: str, entityName: str, **kwargs) -> Response:
    """Add a slot to an intent
    """

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(intentName, str), "intentName parameter must be a string"
    assert isinstance(entityName, str), "entityName parameter must be a string"
    assert isinstance(slotName, str), "slotName parameter must be a string"

    return endpoint("/assistant/intent/slot", {
        **kwargs,
        "assistantId": assistantId,
        "intentName": intentName,
        "entityName": entityName,
        "slotName": slotName,
    }, method="put")
