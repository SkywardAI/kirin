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

class MethodKit:
    """
    A class that contains http methods for the HTTPKit class.
    """

    def __init__(self):
        raise EnvironmentError(
            "This MethodKit is not meant to be instantiated. Use the methods directly."
        )

    @classmethod
    def http_post(cls, *args, **kwargs)-> httpx.Response:
        """
        Post request with httpx client.

        Args:
        *args: Variable length argument list.
        **kwargs: Arbitrary keyword arguments.
            * url: URL to post to.
            * json: JSON data to post.
            * headers: Headers to send.
            * timeout: Timeout for the request.

        Returns:
        httpx.Response: Response from the server.
        """
        url = kwargs.get("url")
        jason_content = kwargs.get("json")
        headers = kwargs.get("headers")
        timeout = kwargs.get("timeout")

        with httpx.Client() as client:
            res = client.post(
                url,
                headers=headers,
                json=jason_content,
                timeout=timeout
            )

            res.raise_for_status()
            return res
