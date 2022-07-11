"""
Copyright (c) 2022 Philipp Scheer
"""


import re
import json
import time
import requests
from rockeet import getToken, baseUrl, logger


class AttributeDict(dict):
    def __init__(self, *args, **kwargs):
        super(AttributeDict, self).__init__(*args, **kwargs)
        self.__dict__ = self


class Response:
    def __init__(self, data, sourceUrl: str, sourceBody, sourceMethod: str, raw: bool = False, time: float = 0) -> None:
        self.data = data
        self.sUrl = sourceUrl
        self.sBody = sourceBody
        self.sMethod = sourceMethod
        self.sTime = time
        if not raw and not self.success:
            raise ValueError(f"request failed: {self.sMethod}@{self.sUrl} ({self.sBody}) -> {self.data}")
    
    @property
    def success(self):
        return self.data["success"]
    
    @property
    def result(self):
        return self.data["result"]

    def unpack(self, *params):
        if isinstance(self.result, dict):
            return { k:v for k,v in self.result.items() if k in params }
        elif isinstance(self.result, list):
            raise ValueError("cannot unpack list")
        return { k: self.result for k in params }

    def items(self):
        return self.result.items()

    def __len__(self):
        return len(self.result)

    def __getattr__(self, key: str):
        print(self.data, key)
        return self.data[key]

    def __getitem__(self, item):
        return self.result[item]

    def __str__(self) -> str:
        return json.dumps(self.result, indent=4)



def isFileId(tester: str):
    if not isinstance(tester, str):
        return False
    return bool(re.match(r'^(f_|p_|a_)[a-fA-F0-9]+$', tester))

def isLocalFile(tester: str):
    if not isinstance(tester, str):
        return False
    return not isFileId(tester)

def endpoint(url, body, method: str = "post", raw: bool = False) -> Response:
    logger.debug(f"ENDPOINT | endpoint {url} method={method}, body={json.dumps(body, indent=4)}")
    result = None
    start = time.time()
    if raw:
        result = requests.request(method.lower(), baseUrl + url, 
            json=body,
            headers={ "Authorization": getToken() }
        )
    else:
        result = requests.request(method.lower(), baseUrl + url, 
            json=body,
            headers={ "Authorization": getToken() }
        ).json()
    logger.debug(f"ENDPOINT |took {time.time() - start:.5f} seconds")
    return Response(result, url, body, method, raw)
