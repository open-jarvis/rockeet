"""
Copyright (c) 2022 Philipp Scheer
"""


import requests
from rockeet import getToken, baseUrl, logger
from rockeet.helper import RawStringResponse, Response


def upload(localPath: str) -> Response:
    """Upload a file to the Rockeet server to perform various operations"""
    logger.debug(f"calling endpoint post -> /file (file=@{localPath})")
    resp: dict = requests.post(baseUrl + "/file", 
        headers = { "Authorization": getToken() },
        files   = { "file": open(localPath, "rb") }, 
    ).json()


    res = RawStringResponse(resp, "/file", None, "post")
    return res