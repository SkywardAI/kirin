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

from src.utillities httpkit import MethodKit


def test_http_post()-> None:
    """
    Test the http_post method.

    In this test case we calculate the the length of tokens of the content "Hello, World!".

    """
    url = "http://llamacpp:8080/tokenize"
    jason_content = {"content": "Hello, World!"}
    headers={'Content-Type': 'application/json'}
    timeout = 10

    res = MethodKit.http_post(
        url=url,
        jason_content=jason_content,
        headers=headers,
        timeout=timeout
    )

    assert res.status_code == 200
    # length of token is a integer
    assert isinstance(res.json().get('tokens'), int)
