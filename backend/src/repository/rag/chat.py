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

from typing import Any
from collections.abc import AsyncGenerator
import loguru
import httpx

from src.repository.rag.base import BaseRAGRepository
from src.repository.inference_eng import InferenceHelper
from src.utilities.httpkit.httpx_kit import httpx_kit
from src.repository.vector_database import vector_db
from src.utilities.formatters.ds_formatter import DatasetFormatter


class RAGChatModelRepository(BaseRAGRepository):
    async def load_model(self, session_id: int, model_name: str) -> bool:
        """
        TODO: Load the model into the memory
        """
        try:
            pass
        except Exception as e:
            loguru.logger.info(f"Exception --- {e}")
            return False
        return True

    def format_prompt(self, prmpt: str, current_context: str = InferenceHelper.instruction) -> str:
        """
        Format the input questions, can be used for saving the conversation history

        Args:
        prmpt (str): input message
        current_context (str): the context we got from the vector database

        Returns:
        str: formatted prompt
        """
        return f"### System: {current_context}\n" + f"\n### Human: {prmpt}\n### Assistant:"

    async def inference(
        self,
        session_uuid: str,
        input_msg: str,
        temperature: float = 0.2,
        top_k: int = 40,
        top_p: float = 0.9,
        n_predict: int = 128,
    ) -> AsyncGenerator[Any, None]:
        """
        **Inference using seperate service:(llamacpp)**

        **Args:**
        - **session_id (int):** session id
        - **input_msg (str):** input message
        - **chat_repo:** chat repository
        - **temperature (float):** temperature for inference(float)
        - **top_k (int):** top_k parameter for inference(int)
        - **top_p (float):** top_p parameter for inference(float)
        - **n_predict (int):** n_predict parameter for inference(int)

        **Returns:**
        AsyncGenerator[Any, None]: response message
        """

        data = {
            "prompt": self.format_prompt(input_msg),
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "n_keep": 0,  # If the context window is full, we keep 0 tokens
            "n_predict": 128 if n_predict == 0 else n_predict,
            "cache_prompt": True,
            "slot_id": -1,  # for cached prompt
            "stop": ["\n### Human:"],
            "stream": True,
        }

        try:
            async with httpx_kit.async_client.stream(
                "POST",
                InferenceHelper.instruct_infer_url(),
                headers={"Content-Type": "application/json"},
                json=data,
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

    def search_context(self, input_msg: str, collection_name: str) -> str:
        """
        Search the context from the vector database

        Args:
        input_msg (str): input message
        collection_name (str): collection name

        Returns:
        str: context
        """
        try:
            res = httpx_kit.sync_client.post(
                InferenceHelper.instruct_embedding_url(),
                headers={"Content-Type": "application/json"},
                json={"content": input_msg},
                timeout=httpx.Timeout(timeout=None),
            )
            res.raise_for_status()
            embedd_input = res.json().get("embedding")
        except Exception as e:
            loguru.logger.error(e)
        # collection name for testing
        context = vector_db.search(
            list(embedd_input), 1, table_name=DatasetFormatter.format_dataset_by_name(collection_name)
        )
        return context

    async def inference_with_rag(
        self,
        input_msg: str,
        collection_name: str,
        temperature: float = 0.2,
        top_k: int = 40,
        top_p: float = 0.9,
        n_predict: int = 128,
    ) -> AsyncGenerator[Any, None]:
        """
        Inference using RAG

        Returns:
        AsyncGenerator[Any, None]: response message
        """

        async def get_context_by_question(input_msg: str):
            """
            Get the context from v-db by the question
            """

            try:
                res = await httpx_kit.async_client.post(
                    InferenceHelper.instruct_embedding_url(),
                    headers={"Content-Type": "application/json"},
                    json={"content": input_msg},
                    timeout=httpx.Timeout(timeout=None),
                )
                res.raise_for_status()
                embedd_input = res.json().get("embedding")
            except Exception as e:
                loguru.logger.error(e)
            # collection name for testing
            context = vector_db.search(
                list(embedd_input), 1, table_name=DatasetFormatter.format_dataset_by_name(collection_name)
            )
            if context:
                context = f"Please answer the question based on answer {context}"
            else:
                context = InferenceHelper.instruction
            loguru.logger.info(f"Context: {context}")
            return context

        current_context = await get_context_by_question(input_msg)

        data_with_context = {
            "prompt": self.format_prompt(input_msg, current_context=current_context),
            "temperature": temperature,
            "top_k": top_k,
            "top_p": top_p,
            "n_keep": 0,  # If the context window is full, we keep 0 tokens
            "n_predict": 128 if n_predict == 0 else n_predict,
            "cache_prompt": False,
            "slot_id": -1,  # for cached prompt
            "stop": ["\n### Human:"],
            "stream": True,
        }

        try:
            async with httpx_kit.async_client.stream(
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
