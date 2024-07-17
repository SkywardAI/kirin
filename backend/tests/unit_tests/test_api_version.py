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

import unittest
import fastapi
from fastapi.testclient import TestClient
from src.api.routes import version


class TestAPIVersion(unittest.TestCase):
    """
    Test the FastAPI application attributes
    """
    
    @classmethod
    def setUpClass(cls):
        cls.app = fastapi.FastAPI()
        cls.app.include_router(version.router)
        cls.client = TestClient(cls.app)
    
    @classmethod
    def tearDownClass(cls):
        pass

    def test_api_version(self):
        """
        Test the version API
        """
        response = self.client.get("/version")
        assert response.status_code == 200
        assert response.json() == {
            "inferenceEngine": "server--b1-2321a5e",
            "milvus": "v2.3.12",
            "kirin": "v0.1.15",
        }







