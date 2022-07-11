"""
Copyright (c) 2022 Philipp Scheer
"""


import sys
from typing import Literal, Union
from rockeet.helper import Response, endpoint, isFileId

from rockeet.Assistant._entity._add import addEntity as _addEntity
from rockeet.Assistant._entity._delete import deleteEntity as _deleteEntity
from rockeet.Assistant._entity._export import exportEntity as _exportEntity
from rockeet.Assistant._entity._list import allEntites as _allEntites

from rockeet.Assistant._utterance._add import addUtterance as _addUtterance
from rockeet.Assistant._utterance._delete import deleteUtterance as _deleteUtterance
from rockeet.Assistant._utterance._list import allUtterances as _allUtterances

from rockeet.Assistant._intent._add import addIntent as _addIntent
from rockeet.Assistant._intent._delete import deleteIntent as _deleteIntent
from rockeet.Assistant._intent._list import allIntents as _allIntents

from rockeet.Assistant._slot._add import addSlot as _addSlot
from rockeet.Assistant._slot._delete import deleteSlot as _deleteSlot
from rockeet.Assistant._slot._list import allSlots as _allSlots

from rockeet.Assistant._assistant._train import train as _train
from rockeet.Assistant._assistant._parse import parse as _parse
from rockeet.Assistant._assistant._delete import deleteAssistant as _deleteAssistant


class Assistant(sys.modules[__name__].__class__):
    def __init__(self, source: Union[Response,str]) -> None:
        self.id = None

        if isinstance(source, Response):
            self.id = source.unpack("assistantId")["assistantId"]
        elif isFileId(source):
            self.id = source
        else:
            raise ValueError("""source must be a Response or the id of an existing assistant.
Alternatively you can create a new assistant using:
  import rockeet
  rockeet.Assistant(name, language, metadata)""")

    def __call__(self, name: str, language: Literal["en", "de", "es", "fr", "it"] = None, metadata: dict = {}):
        if language is None:
            if not isinstance(name, Response) and not isFileId(name):
                raise ValueError("""the language must be set to either "en", "de", "es", "fr", "it".
Want to initialize an existing assistant?
  import rockeet
  rockeet.Assistant(existingAssistantId)""")
            return Assistant(source=name)
        return newAssistant(name, language, metadata)

    def __str__(self) -> str:
        return f"Assistant(id={self.id})"


    def addEntity(self, name: str, examples: list, autoExtend: bool = True, useSynonyms: bool = True, strictness: float = 0.8, metadata: dict = {}) -> Response:
        return _addEntity(self.id, name, examples, autoExtend, useSynonyms, strictness, metadata)

    def deleteEntity(self, name: str, **kwargs) -> Response:
        return _deleteEntity(self.id, name, **kwargs)
    
    def exportEntity(self, name: str, **kwargs) -> object:
        return _exportEntity(self.id, name, **kwargs)

    def allEntites(self, expand: list[Literal["examples", "autoExtend", "useSynonyms", "strictness", "metadata"]] = []) -> Response:
        return _allEntites(self.id, expand)


    def addIntent(self, name: str, slots: dict, utterances: list, metadata: dict = {}) -> Response:
        return _addIntent(self.id, name, slots, utterances, metadata)

    def deleteIntent(self, name: str, **kwargs) -> Response:
        return _deleteIntent(self.id, name, **kwargs)

    def allIntents(self, expand: list[Literal["slots", "utterances", "metadata"]] = []) -> Response:
        return _allIntents(self.id, expand)


    def addSlot(self, intentName: str, entityName: str, slotName: str, **kwargs) -> Response:
        return _addSlot(self.id, intentName, entityName, slotName, **kwargs)

    def deleteSlot(self, intentName: str, slotName: str, **kwargs) -> Response:
        return _deleteSlot(self.id, intentName, slotName, **kwargs)

    def allSlots(self, intentName: str, expand: bool = True, **kwargs) -> Response:
        return _allSlots(self.id, intentName, expand, **kwargs)


    def addUtterance(self, intentName: str, utterance: Union[list,str], index: int = None, **kwargs) -> Response:
        return _addUtterance(self.id, intentName, utterance, index, **kwargs)

    def deleteUtterance(self, intentName: str, index: int = None, **kwargs) -> Response:
        return _deleteUtterance(self.id, intentName, index, **kwargs)

    def allUtterances(self, intentName: str, **kwargs) -> Response:
        return _allUtterances(self.id, intentName, **kwargs)


    def delete(self):
        return _deleteAssistant(self.id)

    def train(self) -> Response:
        return _train(self.id)
    
    def parse(self, input: str) -> Response:
        return _parse(self.id, input)


def newAssistant(name: str, language: Literal["en", "de", "es", "fr", "it"], metadata: dict = {}) -> Assistant:
    """Create a new conversational assistant.
    """

    assert language in ["en", "de", "es", "fr", "it"], "language parameter must be one of 'en', 'de', 'es', 'fr', 'it'"
    assert isinstance(name, str), "name parameter must be a string"
    assert isinstance(metadata, dict), "metadata parameter must be a dictionary"

    assistant = endpoint("/assistant", {
        "name": name,
        "language": language,
        "metadata": metadata
    })

    return Assistant(assistant)
