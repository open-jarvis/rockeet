"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet.helper import Response, endpoint, isFileId, isLocalFile
from rockeet.File import upload


def speakers(fileId: Union[str, Response], profiles: list[Union[str, Response]], allChunks: bool = False, allScores: bool = False, unknownThreshold: float = 0.75, rate: int = 16) -> Response:
    """Identify speakers in an audio recording with their timestamps.
    Note:
    Use a wave file for faster processing.
    If `allChunks` is set to true, no grouping will be performed and all chunks will be returned.
    If `allChunks` is set to false, the speaker will be returned with when he started and stopped speaking.
    If `allScores` is set, all similarity scores will be returned. Otherwise, only the best score will be returned.
    :param unknownThreshold: defines the similarity threshold for the unknown speaker. If the similarity score is below this value, the speaker is considered unknown.
    :param rate: defines the number of chunks per second. A higher value means that more chunks are generated and the diarization is more accurate but also slower.
    """

    assert len(profiles) > 0, "at least one valid profile required"

    for i in range(len(profiles)):
        profile = profiles[i]
        if isinstance(profile, Response):
            profiles[i] = profile.unpack("fileId")["fileId"]

    if isLocalFile(fileId):
        fileId = upload(fileId)
    
    if isinstance(fileId, Response):
        fileId = fileId.unpack("fileId")["fileId"]
    
    if not isFileId(fileId):
        raise ValueError("fileId must be a valid fileId")

    body = {
        "fileId": fileId,
        "profiles": profiles,
        "allChunks": allChunks,
        "allScores": allScores,
        "unknownThreshold": unknownThreshold,
        "rate": rate,
    }

    return endpoint("/audio/speakers", body, method="post")


identify, identify_speakers, identifySpeakers = speakers, speakers, speakers