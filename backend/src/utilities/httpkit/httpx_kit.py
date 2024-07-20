# coding=utf-8

# Copyright [2024] [SkywardAI]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#        http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import httpx


class HttpxKit:
    """
    A class to initialize an async and sync client using httpx

    We only create one client every time is efficient and easy to manage

    Note: We don't close client because we want to keep the connection alive, I don't know if it will cause any problem in more bigger scale
    """

    def __init__(self):
        self.async_client = self.init_async_client()
        self.sync_client = self.init_sync_client()

    def init_async_client(self) -> httpx.AsyncClient:
        """
        Create async client by using Singleletton pattern

        Replace the code below:

        async with httpx.AsyncClient() as client:
            try:
                async with client.stream(
                    "POST",
                    InferenceHelper.instruct_infer_url(),
                    headers={"Content-Type": "application/json"},
                    json=data_with_context,
                    # We disable all timeout and trying to fix streaming randomly cutting off
                    timeout=httpx.Timeout(timeout=None),
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_text():
                        yield chunk
            except httpx.ReadError as e:
                loguru.logger.error(f"An error occurred while requesting {e.request.url!r}.")
            except httpx.HTTPStatusError as e:
                loguru.logger.error(f"Error response {e.response.status_code} while requesting {e.request.url!r}.")

        Returns:
        httpx.AsyncClient: An async client
        """
        return httpx.AsyncClient()

    def init_sync_client(self):
        """
        Create sync client client by using Singleletton pattern

        Returns:
        httpx.Client: A sync client
        """
        return httpx.Client()

    async def teardown_async_client(self) -> bool:
        """
        Close the async client
        """
        await self.async_client.aclose()
        return self.async_client.is_closed

    def teardown_sync_client(self) -> bool:
        """
        Close the sync client

        Returns:
        *
        """
        self.sync_client.close()
        return self.sync_client.is_closed


httpx_kit = HttpxKit()
