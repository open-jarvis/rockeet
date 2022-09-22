"""
Copyright (c) 2022 Philipp Scheer
"""


import os
import mimetypes
from tempfile import NamedTemporaryFile
from typing import Union
from rockeet.helper import RawStringResponse, Response, endpoint, isFileId, isLocalFile
from rockeet.File import upload, delete
from rockeet import logger


def wave(localFile: Union[str, Response], contentType: str = None, doLocally: bool = False, keepOriginal: bool = False) -> Response:
    """Convert an audio file to wave format.
    Audio files in wave format are faster to process by other endpoints
    """

    uploadedFile = False

    if not isLocalFile(localFile) and doLocally:
        logger.warn("cannot convert remote file on local system, falling back to online conversion")

    if isLocalFile(localFile) and doLocally:
        contentType_, _ = mimetypes.guess_type(localFile)
        logger.debug(f"detected contentType: {contentType_}")
        try:
            from pydub import AudioSegment
            convert = True
            fn = None
            if contentType_ == "audio/mpeg":
                fn = AudioSegment.from_mp3
            elif contentType_ == "video/x-flv":
                fn = AudioSegment.from_flv
            elif contentType_ == "audio/ogg":
                fn = AudioSegment.from_ogg
            elif contentType_ == "audio/pcm":
                fn = AudioSegment.from_raw
            elif contentType_ == "audio/wav":
                fn = AudioSegment.from_wav
                convert = False

            if fn is None:
                raise RuntimeError(f"failed to convert file offline, could not guess mimetype for {localFile}")

            sound = fn(localFile)

            if convert:
                tmpFile = NamedTemporaryFile(mode="wb", delete=False, suffix=f"_{os.path.basename(localFile)}.wav")
                logger.debug(f"temporary file created: {tmpFile.name}")
                sound.get(tmpFile.name, format="wav")
                localFile = tmpFile.name
            else:
                logger.warn("skipping conversion, file is already in wav format")
            
            return upload(localFile)
        except ImportError:
            logger.warn("pydub is not installed, falling back to online conversion\ninstall pydub with `pip install pydub`")
            doLocally = False

    if isLocalFile(localFile):
        logger.info("uploading local audio file")
        localFile = upload(localFile)
        uploadedFile = True

    if isinstance(localFile, Response):
        localFile = localFile.unpack("fileId")["fileId"]
        logger.debug(f"unpacking response, fileId: {localFile}")

    if not isFileId(localFile):
        raise ValueError("Invalid fileId")

    body = { "fileId": localFile }
    if contentType is not None:
        if contentType in ["audio/mpeg", "video/x-flv", "audio/ogg", "audio/pcm", "audio/wav"]:
            body["contentType"] = contentType
        else:
            logger.warn("invalid contentType, must be in [\"audio/mpeg\", \"video/x-flv\", \"audio/ogg\", \"audio/pcm\", \"audio/wav\"], falling back to default")

    result = endpoint(f"/audio/wave", body=body, method="post", ResponseClass=RawStringResponse)

    if uploadedFile and not keepOriginal:
        logger.info("deleting uploaded audio file")
        delete(localFile)

    return result


toWave = wave
to_wave = wave
