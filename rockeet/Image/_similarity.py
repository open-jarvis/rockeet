"""
Copyright (c) 2022 Philipp Scheer
"""


from typing import Union
from rockeet import logger
from rockeet.helper import Response, endpoint


def similarity(profile1: Union[Response,str], profile2: Union[Response,str], range: bool = False, **kwargs) -> Response:
    """Create a face profile for a person"""

    allowedEndpoints = ["/image/faces"]
    displayWarn = False
    if isinstance(profile1, Response):
        assert profile1.sUrl in allowedEndpoints, f"a face profile can only be created from one of the following endpoints: {', '.join(allowedEndpoints)}"
        profile1 = profile1.result
        assert len(profile1) > 0, "no face detected"
        profile1 = profile1[0]
    else:
        displayWarn = True

    if isinstance(profile2, Response):
        assert profile2.sUrl in allowedEndpoints, f"a face profile can only be created from one of the following endpoints: {', '.join(allowedEndpoints)}"
        # when the request comes directly from /image/faces, use the fileId in the request
        profile2 = profile2.result
        assert len(profile2) > 0, "no face detected"
        profile2 = profile2[0]
    else:
        displayWarn = True

    if displayWarn:
        logger.warn(f"you're importing your own profile\nthis is not recommended and might lead to weird results")

    logger.info(f"checking similarity of faces")

    return endpoint("/image/similarity", {
        **kwargs,
        "range": range,
        "profile1": profile1["profile"] if isinstance(profile1, dict) else profile1,
        "profile2": profile2["profile"] if isinstance(profile2, dict) else profile2
    })
