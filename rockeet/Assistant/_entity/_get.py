"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def getEntity(assistantId: str, entityName: str, **kwargs) -> Response:
    """Get an entity"""

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(entityName, str), "entityName parameter must be a string"

    return endpoint("/assistant/entity", {
        **kwargs,
        "assistantId": assistantId,
        "entityName": entityName,
    }, method="get")
