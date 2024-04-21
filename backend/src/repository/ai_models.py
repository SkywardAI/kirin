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

import os

from kimchima.pkg import (
    ModelFactory,
    TokenizerFactory,
    EmbeddingsFactory,
    PipelinesFactory
)
from kimchima.utils import (
    Dialog,
    Downloader
)

from src.config.settings.const import DEFAULT_ENCODER, DEFAULT_MODEL, DEFAUTL_SUMMERIZE_MODEL,DEFAULT_MODEL_PATH


class ModelPipeline:
    r"""
    ModelPipeline class:
    - to compute embeddings by using the encoder model
    - to generate an answer by using the transformers pipeline.
    """

    async def init(self, model_name=DEFAULT_MODEL,model_sum=DEFAUTL_SUMMERIZE_MODEL, encoder_name=DEFAULT_ENCODER) -> None:
        #TODO Logger system
        self.pipe, self.tokenizer = self.initialize_pipeline(model_name)
        self.pipe_con = self.initialize_pip_con(model_name)
        self.pipe_sum = self.initialize_pip_sum(model_sum)
        self.encoder_model, self.encoder_tokenizer = self.initialize_encoder(encoder_name)
        self.model_name = model_name
        # self.initialize_encoder(DEFAULT_ENCODER)

    def encode_string(self, data):
        embeddings=EmbeddingsFactory.get_text_embeddings(
            model=self.encoder_model,
            tokenizer=self.encoder_tokenizer,
            prompt=data,
            device="cpu",
            max_length=512,
        )

        return embeddings
    

    def initialize_encoder(self, encoder_name):
        model_path = self._check_and_download_model(encoder_name)
        encoder_model=ModelFactory.auto_model(pretrained_model_name_or_path=model_path)
        tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=model_path)
        return encoder_model, tokenizer


    def initialize_pip_con(self, model_name):
        model_path = self._check_and_download_model(model_name)
        tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=model_path)
        pip = PipelinesFactory.customized_pipe(model=model_path,
                                               tokenizer=tokenizer,
                                               device_map='auto',
                                               task="conversational")
        return pip

    def initialize_pip_sum(self, model_name):
        model_path = self._check_and_download_model(model_name)
        tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=model_path)
        pip = PipelinesFactory.customized_pipe(model=model_path,
                                               tokenizer=tokenizer,
                                               device_map='auto',
                                               task="summarization")
        return pip

    def initialize_pipeline(self, model_name):
        r"""
        Initialize the pipeline by using tokenizer and model
        """
        model_path = self._check_and_download_model(model_name)
        tokenizer= TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=model_path)

        # handle multiple steps internally, like tokenizing, feeding tokens into model, and processing the output into a human-readble form
        pipe= PipelinesFactory.text_generation(
            model=model_path,
            tokenizer=tokenizer,
            trust_remote_code=True,
            max_new_tokens=50
        )

        return pipe, tokenizer

    def generate_conversation(self, chat_history, question):
        r"""
        Inference by using transformers pipeline
        """
        if len(chat_history) == 0:
            return PipelinesFactory.init_conversation(question)
        #Use the first
        con = PipelinesFactory.init_conversation(chat_history[0].message)
        for i in range(1, len(chat_history)):
            role="assistant" if chat_history[i].is_bot_msg else "user"
            con.add_message({"role": role, "content": chat_history[i].message})
        con.add_message({"role": "user", "content": question})
        return con
        

    def generate_answer(self, messages, prompt=None):
        r"""
        Inference by using transformers pipeline
        """
        res = Dialog.chat_summary(
            pipe_con=self.pipe_con,
            pipe_sum=self.pipe_sum,
            messages=messages,
            prompt=prompt
            )
        # TODO logger
        return res

    def _check_and_download_model(self, model_name):
        r"""
        Check the model exists or not, if not download the model
        """
        model_path = DEFAULT_MODEL_PATH + model_name
        if os.path.exists(model_path):
            return model_path
        else:
            Downloader.auto_downloader(model_name=model_name, folder_name=model_path)
            return model_path


ai_model: ModelPipeline = ModelPipeline()
