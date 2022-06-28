"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet.helper import Response, endpoint, isFileId, isLocalFile
from rockeet.File import upload


def profile(fileId: Union[str, Response], name: str, metadata: dict = {}, start: float = None, end: float = None) -> Response:
    """Create a voice profile of a speaker to identifier him/her in a recording.
    Make sure the audio file provided contains at least 5 seconds of continous speech from the person you'd like to identify.
    This profile can then be used with the /audio/identify endpoint to identify one or more speakers in a recording.
    Note: Use a wave file for faster processing.
    When start and end are set, the file will be sliced accordingly.
    When either start or end is not set, the file will be sliced from the beginning or till the end of the file respectively.
    When neither start nor end are set, the profile will be created for the entire audio file.

    :param fileId: (required) A profile will be created for this audio file
    :param name: (required) The name of the person speaking
    :param metadata: Additional metadata that will be stored with the profile
    :param start: Starting second of the person speaking
    :param end: Ending second of the person speaking
    """

    if isLocalFile(fileId):
        fileId = upload(fileId)
    
    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]
    
    if not isFileId(fileId):
        raise ValueError("fileId must be a valid fileId")

    body = {
        "fileId": fileId,
        "name": name,
        "metadata": metadata
    }
    if start is not None:
        body["start"] = start
    if end is not None:
        body["end"] = end

    return endpoint("/audio/profile", body, method="post")


createProfile, createVoiceProfile, create_profile, create_voice_profile = profile, profile, profile, profile