"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint, isFileId


def parse(assistantId: str, input: str, allScores: bool = False) -> Response:
    """Add an intent to an assistant
    """

    assert isinstance(assistantId, str) and isFileId(assistantId), "assistantId parameter must be a valid assistant id"
    assert isinstance(input, str), "input parameter must be a string"
    assert isinstance(allScores, bool), "allScores parameter must be a boolean"

    return endpoint("/assistant/parse", {
        "assistantId": assistantId,
        "input": input,
        "allScores": allScores,
    })
