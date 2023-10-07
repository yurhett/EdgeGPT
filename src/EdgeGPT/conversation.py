import json
import os
from typing import List, Union

import httpx

from .constants import HEADERS_INIT_CONVER, BUNDLE_VERSION
from .exceptions import NotAllowedToAccess


class Conversation:
    def __init__(
        self,
        proxy: Union[str, None] = None,
        async_mode: bool = False,
        cookies: Union[List[dict], None] = None,
    ) -> None:
        if async_mode:
            return
        self.struct: dict = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        self.proxy = proxy
        proxy = (
            proxy
            or os.environ.get("all_proxy")
            or os.environ.get("ALL_PROXY")
            or os.environ.get("https_proxy")
            or os.environ.get("HTTPS_PROXY")
            or None
        )
        if proxy is not None and proxy.startswith("socks5h://"):
            proxy = "socks5://" + proxy[len("socks5h://") :]
        self.session = httpx.Client(
            verify=False,
            proxies=proxy,
            timeout=900,
            headers=HEADERS_INIT_CONVER,
        )
        if cookies:
            for cookie in cookies:
                self.session.cookies.set(cookie["name"], cookie["value"])
        request_url = os.environ.get("BING_PROXY_URL") or "https://edgeservices.bing.com/edgesvc/turing/conversation/create"
        request_url = f"{request_url}?bundleVersion={BUNDLE_VERSION}"
        # Send GET request
        response = self.session.get(
            url=request_url,
        )
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(response.text)
            print(response.url)
            raise Exception("Authentication failed")
        try:
            self.struct = response.json()
            print(self.struct)
        except (json.decoder.JSONDecodeError, NotAllowedToAccess) as exc:
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc
        if self.struct["result"]["value"] == "UnauthorizedRequest":
            raise NotAllowedToAccess(self.struct["result"]["message"])
        if 'X-Sydney-Encryptedconversationsignature' in response.headers:
            self.struct['sec_access_token'] = response.headers['X-Sydney-Encryptedconversationsignature']

    @staticmethod
    async def create(
        proxy: Union[str, None] = None,
        cookies: Union[List[dict], None] = None,
    ) -> "Conversation":
        self = Conversation(async_mode=True)
        self.struct = {
            "conversationId": None,
            "clientId": None,
            "conversationSignature": None,
            "result": {"value": "Success", "message": None},
        }
        self.proxy = proxy
        proxy = (
            proxy
            or os.environ.get("all_proxy")
            or os.environ.get("ALL_PROXY")
            or os.environ.get("https_proxy")
            or os.environ.get("HTTPS_PROXY")
            or None
        )
        if proxy is not None and proxy.startswith("socks5h://"):
            proxy = "socks5://" + proxy[len("socks5h://") :]
        transport = httpx.AsyncHTTPTransport(retries=900)
        # Convert cookie format to httpx format
        formatted_cookies = None
        if cookies:
            formatted_cookies = httpx.Cookies()
            for cookie in cookies:
                # Fix: Use full cookies not only _U and SUID
                # if cookie["name"] in ["_U", "SUID"]:
                formatted_cookies.set(cookie["name"], cookie["value"])
        async with httpx.AsyncClient(
            proxies=proxy,
            timeout=30,
            headers=HEADERS_INIT_CONVER,
            transport=transport,
            cookies=formatted_cookies,
            verify=False,
        ) as client:
            # Send GET request
            request_url = os.environ.get("BING_PROXY_URL") or "https://www.bing.com/turing/conversation/create"
            request_url = f"{request_url}?bundleVersion={BUNDLE_VERSION}"
            response = await client.get(
                url=request_url,
                follow_redirects=True,
            )
        if response.status_code != 200:
            print(f"Status code: {response.status_code}")
            print(response.text)
            print(response.url)
            raise Exception("Authentication failed")
        try:
            self.struct = response.json()
        except (json.decoder.JSONDecodeError, NotAllowedToAccess) as exc:
            raise Exception(
                "Authentication failed. You have not been accepted into the beta.",
            ) from exc
        if self.struct["result"]["value"] == "UnauthorizedRequest":
            print(self.struct)
            raise NotAllowedToAccess(self.struct["result"]["value"])
        return self