"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet import logger
from rockeet.File import upload, delete
from rockeet.helper import Response, isLocalFile, endpoint


def faces(fileId: Union[Response,str], sensitivity: float = None, nms: float = None, scale: float = None, keepImage: bool=False, **kwargs) -> Response:
    """Detect faces in an image"""

    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]

    logger.info(f"identifying faces in file {fileId}, {sensitivity=}, {nms=}, {scale=}")

    deleteFileId = False
    obj = { **kwargs,
            "fileId": fileId }

    if isLocalFile(fileId):
        # temporarily upload the file, delete after the operation
        resp = upload(fileId)
        logger.debug(f"uploaded local file '{fileId}' to create fileId '{fileId}'")
        deleteFileId = True
        obj = { **kwargs,
                **resp.unpack("fileId") }
        fileId = resp.unpack("fileId")["fileId"]

    if nms is not None: obj["nms"] = nms
    if scale is not None: obj["scale"] = scale
    if sensitivity is not None: obj["sensitivity"] = sensitivity

    resp = endpoint("/image/faces", obj)

    if deleteFileId and not keepImage:
        logger.debug(f"deleting uploaded file '{fileId}' because it was a local file previously")
        delete(fileId)

    return resp