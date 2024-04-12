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
    PipelinesFactory
)

from src.config.settings.const import DEFAULT_ENCODER, DEFAULT_MODEL, DEFAULT_MODEL_PATH


class ModelPipeline:
    r"""
    ModelPipeline class:
    - to compute embeddings by using the encoder model
    - to generate an answer by using the transformers pipeline.
    """

    def __init__(self, model_name=DEFAULT_MODEL):
        #TODO Logger system
        self.pipe, self.tokenizer = self.initialize_pipeline(DEFAULT_MODEL)
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

    def generate_answer(self, prompt):
        r"""
        Inference by using transformers pipeline
        """
        print(f"promptaaa:{prompt}")        
        sequences = self.pipe(
            prompt,
            max_length=50,
            early_stopping=True,
            truncation=True,
            do_sample=True,
            top_k=1,
            no_repeat_ngram_size=2,
            num_return_sequences=1,
            pad_token_id=self.tokenizer.eos_token_id
        )

        res = (
            sequences[0]
            .get("generated_text")
            .replace("string<|endoftext|>", "")
            .replace("<|endoftext|>", "")
            .replace("\n", "")
        )
        # TODO logger
        return res


ai_model: ModelPipeline = ModelPipeline()
