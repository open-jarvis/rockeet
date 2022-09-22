"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def deleteAssistant(assistantId: str) -> Response:
    """Delete an entity"""

    from rockeet.Assistant._assistant._new import Assistant

    if isinstance(assistantId, Response):
        assistantId = assistantId.unpack("assistantId")["assistantId"]

    if isinstance(assistantId, Assistant):
        assistantId = assistantId.id

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"

    return endpoint(f"/assistant", body={ "assistantId": assistantId }, method="delete")
