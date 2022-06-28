"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet import logger
from rockeet.helper import Response, endpoint


def delete(fileId: Union[Response,list,str]) -> Union[Response,None]:
    """Delete a file given its `fileId`"""

    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]

    if isinstance(fileId, list):
        for fileId_ in fileId:
            if isinstance(fileId_, Response):
                try:
                    fileId_ = fileId_.unpack("fileId")["fileId"]
                except ValueError:
                    logger.warn(f"unable to identify file, not deleting")
                    continue
            endpoint(f"/file/{fileId_}", body={}, method="delete")
    else:
        return endpoint(f"/file/{fileId}", body={}, method="delete")
