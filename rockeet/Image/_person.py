"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet import logger
from rockeet.helper import Response, endpoint, isLocalFile
from rockeet.Image import faces


def person(profile: Union[Response,str], name: str, metadata: dict = {}, sensitivity: float = None, nms: float = None, scale: float = None, keepImage: bool = False, **kwargs) -> Response:
    """Create a face profile for a person

    :param profile: Either a response from Image.faces, a profile obtained and saved by Image.faces or a local file path to an image containing exactly one person
    :param name: The name of the person
    :param metadata: Metadata to store with the profile
    """

    if isinstance(profile, Response):
        allowedEndpoints = ["/image/faces"]
        assert profile.sUrl in allowedEndpoints, f"a face profile can only be created from one of the following endpoints: {', '.join(allowedEndpoints)}"
        profile = profile.result
        assert len(profile) > 0, "no face detected"
        profile = profile[0]["profile"]
    elif isinstance(profile, str):
        if isLocalFile(profile):
            profileFaces = faces(profile, sensitivity=sensitivity, nms=nms, scale=scale, keepImage=keepImage)
            return person(profile=profileFaces, name=name, metadata=metadata)
        else:
            logger.warn(f"you're importing your own profile\nthis is not recommended and might lead to weird results")
    else:
        raise ValueError("profile must be Response or string")

    logger.info(f"creating a face profile of {name}")

    return endpoint("/image/person", {
        **kwargs,
        "name": name,
        "metadata": metadata,
        "profile": profile
    })
