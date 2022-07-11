"""
Copyright (c) 2022 Philipp Scheer
"""


"""
assistant POST                     - done
assistant DELETE                   - done
assistants GET                     - done
assistant/entity GET               - done
assistant/entity POST              - done
assistant/entity DELETE            - done
assistant/entities GET             - done
assistant/intent POST              - done
assistant/intent DELETE            - done
assistant/intents GET              - done
assistant/intent/utterance PUT     - done
assistant/intent/utterance DELETE  - done
assistant/intent/utterances GET    - done
assistant/intent/slot PUT          - done
assistant/intent/slot DELETE       - done
assistant/intent/slots GET         - done
assistant/train POST               - done
assistant/parse POST               - done
"""


from ._assistant._new import newAssistant, Assistant
from ._assistant._list import allAssistants
from ._assistant._delete import deleteAssistant
from ._assistant._train import train
from ._assistant._parse import parse

from ._entity._add import addEntity
from ._entity._delete import deleteEntity
from ._entity._export import exportEntity
from ._entity._list import allEntites

from ._utterance._add import addUtterance
from ._utterance._delete import deleteUtterance
from ._utterance._list import allUtterances

from ._intent._add import addIntent
from ._intent._delete import deleteIntent
from ._intent._list import allIntents

from ._slot._add import addSlot
from ._slot._delete import deleteSlot
from ._slot._list import allSlots


import sys

sys.modules[__name__].__class__ = Assistant
