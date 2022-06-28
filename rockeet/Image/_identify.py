"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet import logger
from rockeet.helper import Response, endpoint, isLocalFile
from rockeet.File import upload, delete


def identify(fileId: Union[Response,str],
             profiles: list,
             scale: float = 1,
             sensitivity: float = 0.9,
             nms: float = 0.3,
             similarity: float = 0.9,
             scores: bool = False, 
             **kwargs) -> Response:
    """Create a face profile for a person"""

    deleteUploadedFile = False

    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]

    if isinstance(fileId, str) and isLocalFile(fileId):
        fileId = upload(fileId).unpack("fileId")["fileId"]
        deleteUploadedFile = True

    for i in range(len(profiles)):
        profile = profiles[i]
        if isinstance(profile, Response):
            profiles[i] = profile.unpack("fileId")["fileId"]

    logger.info(f"identify people in {fileId} (out of {len(profiles)} possibilities")

    obj = { **kwargs,
            "fileId": fileId,
            "profiles": profiles,
            "sensitivity": sensitivity,
            "nms": nms,
            "similarity": similarity,
            "scores": scores,
           }
    if scale is not None: obj["scale"] = scale

    result = endpoint("/image/identify", obj)

    if deleteUploadedFile:
        delete(fileId)
    
    return result
