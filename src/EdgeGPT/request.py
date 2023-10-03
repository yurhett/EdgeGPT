import random
import time
import uuid
from datetime import datetime
from typing import Union

from .conversation_style import CONVERSATION_STYLE_TYPE
from .conversation_style import ConversationStyle
from .utilities import get_location_hint_from_locale, get_location_from_locale
from .utilities import get_ran_hex
from .utilities import guess_locale


class ChatHubRequest:
    def __init__(
            self,
            conversation_signature: str,
            client_id: str,
            conversation_id: str,
            invocation_id: int = 3,
    ) -> None:
        self.struct: dict = {}
        self.client_id: str = client_id
        self.conversation_id: str = conversation_id
        self.conversation_signature: str = conversation_signature
        self.invocation_id: int = invocation_id

    def update(
            self,
            prompt: str,
            ipaddress: str,
            conversation_style: CONVERSATION_STYLE_TYPE,
            webpage_context: Union[str, None] = None,
            search_result: bool = False,
            locale: str = guess_locale(),
    ) -> None:
        options = [
            "deepleo",
            "enable_debug_commands",
            "disable_emoji_spoken_text",
            "enablemm",
        ]
        if conversation_style:
            if not isinstance(conversation_style, ConversationStyle):
                conversation_style = getattr(ConversationStyle, conversation_style)
            options = conversation_style.value
        message_id = str(uuid.uuid4())
        # 获取当前时间戳（秒）
        ts = time.time()

        # 获取本地时间和UTC时间的datetime对象
        local_dt = time.localtime(ts)
        utc_dt = time.gmtime(ts)

        # 计算本地时间和UTC时间的秒数差
        offset_seconds = time.mktime(local_dt) - time.mktime(utc_dt)

        # 转换为小时和分钟的差
        offset_hours = int(offset_seconds // 3600)
        offset_minutes = int((offset_seconds % 3600) // 60)

        # 格式化为字符串，如"+08:00"
        if offset_hours >= 0:
            sign = "+"
        else:
            sign = "-"
        offset_string = f"{sign}{abs(offset_hours):02d}:{abs(offset_minutes):02d}"
        # Get current time
        timestamp = datetime.now().strftime("%Y-%m-%dT%H:%M:%S") + offset_string
        self.struct = {
            "arguments": [{
                "source": "cib",
                "optionsSets": options,
                "allowedMessageTypes": [
                    "ActionRequest",
                    "Chat",
                    "Context",
                    "InternalSearchQuery",
                    "InternalSearchResult",
                    "Disengaged",
                    "InternalLoaderMessage",
                    "Progress",
                    "RenderCardRequest",
                    "AdsQuery",
                    "SemanticSerp",
                    "GenerateContentQuery",
                    "SearchQuery"
                ],
                "sliceIds": [
                    "gbacf",
                    "divkorbl2p",
                    "emovoicecf",
                    "tts3cf",
                    "crtrgxnew",
                    "inochatv2",
                    "wrapnoins",
                    "norbingchrome",
                    "sydconfigoptc",
                    "178gentechs0",
                    "824fluxhi52s0",
                    "0825agicert",
                    "0901usrprmpt",
                    "821fluxv13hint",
                    "727nrprdrs0"
                ],
                "verbosity": "verbose",
                "scenario": "SERP",
                "plugins": [],
                "traceId": get_ran_hex(32),
                "isStartOfSession": self.invocation_id == 3,
                "requestId": message_id,
                "message": {
                    "locale": guess_locale(),
                    "market": locale,
                    "region": locale[-2:],
                    "location": get_location_from_locale(locale),
                    "locationHints": get_location_hint_from_locale(locale),
                    "userIpAddress": random.choice([ipaddress, None]),
                    "timestamp": timestamp,
                    "author": "user",
                    "inputMethod": "Keyboard",
                    "text": prompt,
                    "messageType": "Chat",
                    "requestId": message_id,
                    "messageId": message_id
                },
                "tone": conversation_style.name.capitalize(),
                "conversationSignature": self.conversation_signature,
                "participant": {
                    "id": self.client_id,
                },
                "spokenTextMode": "None",
                "conversationId": self.conversation_id
            }],
            "invocationId": str(self.invocation_id),
            "target": "chat",
            "type": 4
        }
        if search_result:
            have_search_result = [
                "InternalSearchQuery",
                "InternalSearchResult",
                "InternalLoaderMessage",
                "RenderCardRequest",
            ]
            self.struct["arguments"][0]["allowedMessageTypes"] += have_search_result
        if webpage_context:
            self.struct["arguments"][0]["previousMessages"] = [
                {
                    "author": "user",
                    "description": webpage_context,
                    "contextType": "WebPage",
                    "messageType": "Context",
                    "messageId": "discover-web--page-ping-mriduna-----",
                },
            ]
        self.invocation_id += 1

        # print(timestamp)
