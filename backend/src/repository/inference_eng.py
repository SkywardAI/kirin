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


# https://pypi.org/project/openai/1.35.5/
import openai

from src.config.manager import settings

class InferenceHelper:
    def init(self) -> None:
        # TODO pydantic settings
        self.infer_eng_url=settings.INFERENCE_ENG
        self.infer_eng_port=settings.INFERENCE_ENG_PORT
        # OpenAI-compatible Chat Completions API
        self.client=self.openai_client()

    
    def openai_client(self) -> openai.OpenAI:
        """
        Initialize OpenAI client
        
        Returns:
        openai.OpenAI: OpenAI client
        
        """
        url=f'http://{self.infer_eng_url}:{self.infer_eng_port}/v1'
        api_key='sk-no-key-required'

        return openai.OpenAI(base_url=url, api_key=api_key)


inference_helper: InferenceHelper = InferenceHelper()