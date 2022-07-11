"""
Copyright (c) 2022 Philipp Scheer
"""


from rockeet.helper import endpoint
from rockeet.Assistant import Assistant


def allAssistants(**kwargs) -> list[Assistant]:
    """List all created assistants"""

    return [ Assistant(a["assistantId"]) for a in endpoint("/assistants", {
        **kwargs,
    }, method="get").result ]
