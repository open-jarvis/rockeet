"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union

from rockeet import logger
from rockeet.helper import isLocalFile, endpoint, Response
from rockeet.File import upload, delete


def faces(fileId: Union[Response,str], sensitivity: float = None, nms: float = None, scale: float = None, detectionFramesPerSecond: int = None, profiles: list = [], **kwargs) -> Response:
    """Detect and track faces in an image"""

    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]

    logger.info(f"identifying faces in video file {fileId}, {sensitivity=}, {nms=}, {scale=}, {detectionFramesPerSecond=}, {profiles=}")

    deleteFileId = False

    if isLocalFile(fileId):
        # temporarily upload the file, delete after the operation
        resp = upload(fileId)
        logger.debug(f"uploaded local file '{fileId}' to create fileId '{fileId}'")
        deleteFileId = True
        obj = { **kwargs,
                **resp.unpack("fileId") }
        fileId = resp.unpack("fileId")["fileId"]

    for index, profile in enumerate(profiles):
        if isinstance(profile, Response):
            assert profile.sUrl in ["/image/person"], "invalid profile (must come from /image/person)"
            profiles[index] = profile.unpack("fileId")["fileId"]

    obj = { **kwargs,
            "profiles": profiles,
            "fileId": fileId }

    if nms is not None: obj["nms"] = nms
    if scale is not None: obj["scale"] = scale
    if sensitivity is not None: obj["sensitivity"] = sensitivity
    if detectionFramesPerSecond is not None: obj["detectionFramesPerSecond"] = detectionFramesPerSecond

    resp = endpoint("/video/faces", obj)

    if deleteFileId:
        logger.debug(f"deleting uploaded file '{fileId}' because it was a local file previously")
        delete(fileId)

    return resp
