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
import jwt as pyjwt

@unittest.skip("Skip this test, it is a evidence of a security vulnerability")
class TestJWTReplacedSolution(unittest.TestCase):

    JWT_SECRET_KEY="YOUR-KEY"
    ALGORITHM="HS256"
    content={"some": "payload"}
    
    @classmethod
    def setUpClass(cls) -> None:
        return super().setUpClass()
    
    @classmethod
    def tearDownClass(cls) -> None:
        return super().tearDownClass()
    

    def test_jwt_jose(self):
        pass
        # jose_str=jose_jwt.encode(self.content, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        
        # pyjwt_str=pyjwt.encode(self.content, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)

        # # jose and pyjwt should produce the same token
        # assert jose_str == pyjwt_str
    
    def test_jwt_decode(self):
        pass
        # jose_str=jose_jwt.encode(self.content, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)
        
        # pyjwt_str=pyjwt.encode(self.content, key=self.JWT_SECRET_KEY, algorithm=self.ALGORITHM)

        # # jose and pyjwt should produce the same token
        # assert jose_str == pyjwt_str

        # # decode the token
        # jose_decoded=jose_jwt.decode(jose_str, key=self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])
        # pyjwt_decoded=pyjwt.decode(pyjwt_str, key=self.JWT_SECRET_KEY, algorithms=[self.ALGORITHM])

        # # jose and pyjwt should produce the same decoded token
        # assert jose_decoded == pyjwt_decoded