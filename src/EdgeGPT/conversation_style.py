from enum import Enum

try:
    from typing import Literal, Union
except ImportError:
    from typing_extensions import Literal
from typing import Optional


class ConversationStyle(Enum):
    creative = [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "dv3sugg",
        "autosave",
        "iyxapbing",
        "iycapbing",
        "h3imaginative",
        "gencontentv3",
        "fluxhint",
        "fluxv13",
        "gcccomp",
        "agicert",
        "iyjbexp",
        "izusrprmpt",
        "eredirecturl"
    ]
    balanced = [
        "nlu_direct_response_filter",
        "deepleo",
        "disable_emoji_spoken_text",
        "responsible_ai_policy_235",
        "enablemm",
        "dv3sugg",
        "autosave",
        "iyxapbing",
        "iycapbing",
        "galileo",
        "gcccomp",
        "agicert",
        "iyjbexp",
        "izusrprmpt",
        "eredirecturl",
        "saharagenconv5",
        "fluxhint",
        "glfluxv13"
    ]
    precise = ["nlu_direct_response_filter",
               "deepleo",
               "disable_emoji_spoken_text",
               "responsible_ai_policy_235",
               "enablemm",
               "dv3sugg",
               "autosave",
               "iyxapbing",
               "iycapbing",
               "h3precise",
               "gcccomp",
               "agicert",
               "iyjbexp",
               "izusrprmpt",
               "eredirecturl",
               "clgalileo",
               "gencontentv3",
               "fluxhint",
               "fluxv13"
    ]


CONVERSATION_STYLE_TYPE = Optional[
    Union[ConversationStyle, Literal["creative", "balanced", "precise"]]
]
