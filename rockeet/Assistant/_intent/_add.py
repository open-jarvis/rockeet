"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def addIntent(assistantId: str, name: str, slots: dict, utterances: list, metadata: dict = {}) -> Response:
    """Add an intent to an assistant
    """

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(name, str), "name parameter must be a string"
    assert isinstance(slots, dict), "slots parameter must be a dict"
    assert isinstance(utterances, list) and len(utterances) > 0, "utterances parameter must be a list with at least one element"
    assert isinstance(metadata, dict), "metadata parameter must be a dictionary"

    for key, value in slots.items():
        if isinstance(value, Response):
            slots[key] = value.unpack("entityId")["entityId"]

    return endpoint("/assistant/intent", {
        "assistantId": assistantId,
        "name": name,
        "slots": slots,
        "utterances": utterances,
        "metadata": metadata,
    })
