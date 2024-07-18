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
        self.instruction=settings.INSTRUCTION
        self.client=self.openai_client() # OpenAI-compatible Chat Completions API
        self.completion_url=self.instruct_infer_url()
        self.tokenization_url=self.instruct_tokenize_url()

    
    def openai_client(self) -> openai.OpenAI:
        """
        Initialize OpenAI client
        
        Returns:
        openai.OpenAI: OpenAI client
        
        """
        url=f'http://{self.infer_eng_url}:{self.infer_eng_port}/v1'
        api_key='sk-no-key-required'
        return openai.OpenAI(base_url=url, api_key=api_key)


    def instruct_tokenize_url(self)->str:
        """
        Get the URL for the tokenization engine

        Returns:
        str: URL for the tokenization
        """
        return f"http://{inference_helper.infer_eng_url}:{inference_helper.infer_eng_port}/tokenize"


    def instruct_infer_url(self)->str:
        """
        Get the URL for the inference engine

        Returns:
        str: URL for the inference engine
        """
        return f"http://{inference_helper.infer_eng_url}:{inference_helper.infer_eng_port}/completion"


inference_helper: InferenceHelper = InferenceHelper()