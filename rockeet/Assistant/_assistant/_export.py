"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import endpoint


def exportAssistant(assistantId: str, **kwargs) -> dict:
    """Export an assistant by id"""

    assert isinstance(assistantId, str) and assistantId.startswith("a_"), f"invalid assistantId {assistantId}"

    return endpoint("/assistant/export", { "assistantId": assistantId }, method="get")


def getAssistant(assistantId: str) -> dict:
    """Get assistant data"""

    assert isinstance(assistantId, str) and assistantId.startswith("a_"), f"invalid assistantId {assistantId}"
    
    return endpoint("/assistant", { "assistantId": assistantId }, method="get")
