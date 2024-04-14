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


from kimchima import (
    ModelFactory,
    TokenizerFactory,
    EmbeddingsFactory,
    PipelinesFactory,
    chat_summary
)

from src.config.settings.const import DEFAULT_ENCODER, DEFAULT_MODEL, DEFAUTL_SUMMERIZE_MODEL


class ModelPipeline:
    r"""
    ModelPipeline class:
    - to compute embeddings by using the encoder model
    - to generate an answer by using the transformers pipeline.
    """

    def __init__(self, model_name=DEFAULT_MODEL):
        #TODO Logger system
        self.pipe, self.tokenizer = self.initialize_pipeline(DEFAULT_MODEL)
        self.model_name = model_name
        # self.initialize_encoder(DEFAULT_ENCODER)

    def encode_string(self, data):
        
        #TODO: It should be load from the local file and set cache in kimchima
        encoder_model=ModelFactory.auto_model(pretrained_model_name_or_path=DEFAULT_ENCODER)
        tokenizer=TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=DEFAULT_ENCODER)

        embeddings=EmbeddingsFactory.get_text_embeddings(
            model=encoder_model,
            tokenizer=tokenizer,
            prompt=data,
            device="cpu",
            max_length=512,
        )

        return embeddings
    

    def initialize_encoder(self, encoder_name):
        # TODO download model by using kimchima Model Gallery
        pass


    def initialize_pipeline(self, model_name):
        r"""
        Initialize the pipeline by using tokenizer and model
        """

        tokenizer= TokenizerFactory.auto_tokenizer(pretrained_model_name_or_path=model_name)

        # handle multiple steps internally, like tokenizing, feeding tokens into model, and processing the output into a human-readble form
        pipe= PipelinesFactory.text_generation(
            model=model_name,
            tokenizer=tokenizer,
            trust_remote_code=True,
            max_new_tokens=50
        )

        return pipe, tokenizer

    def generate_answer(self, messages, prompt=None, model_name=DEFAULT_MODEL):
        r"""
        Inference by using transformers pipeline
        """
        conversation_model=model_name
        summarization_model=DEFAUTL_SUMMERIZE_MODEL
        res = chat_summary(
            conversation_model=conversation_model,
            summarization_model=summarization_model,
            messages=messages,
            prompt=prompt
            )
        # TODO logger
        return res


ai_model: ModelPipeline = ModelPipeline()
