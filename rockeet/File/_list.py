"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import endpoint


def list() -> list:
    """Retrieve a list of all uploaded files"""
    return endpoint(f"/files", body={}, method="get").result
