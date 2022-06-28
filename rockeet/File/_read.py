"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet.helper import Response, endpoint


def read(fileId: Union[Response, str]) -> bytes:
    """Download a file given its `fileId`"""
    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]
    return endpoint(f"/file/{fileId}", body={}, method="get", raw=True).data.content


get = read
download = read
