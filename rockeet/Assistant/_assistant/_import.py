"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import Response, endpoint


def importAssistant(data: dict, **kwargs):
    """Import a previously exported assistant"""
    from rockeet.Assistant._assistant._new import Assistant

    if isinstance(data, Response):
        data = data.unpack("_")["_"]

    assert data[5] == ".", "wrong data format"

    return Assistant(endpoint("/assistant", { "data": data }, method="put"))


