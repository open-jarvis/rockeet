"""
Copyright (c) 2022 Philipp Scheer
"""


import rockeet


def clear(setter=None):
    """Clear the current session.
    """
    return rockeet.setSession(setter)
