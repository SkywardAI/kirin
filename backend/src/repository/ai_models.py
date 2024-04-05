import torch
import transformers
from kimchima import Auto
from transformers import AutoModelForCausalLM, AutoTokenizer

from src.config.settings.const import DEFAULT_ENCODER, DEFAULT_MODEL, DEFAULT_MODEL_PATH


class ModelPipeline:
    def __init__(self, model_name=DEFAULT_MODEL):
        print("start init model")
        self.pipeline, self.tokenizer = self.initialize_model(DEFAULT_MODEL)
        self.initialize_encoder(DEFAULT_ENCODER)

    def encode_string(self, data):
        embeddings = self.encoder.get_embeddings(text=data)
        return embeddings

    def initialize_encoder(self, model_name):
        self.encoder = Auto(model_name_or_path=model_name)

    def initialize_model(self, model_name):

        # model = AutoModelForCausalLM.from_pretrained(model_name)
        # tokenizer = AutoTokenizer.from_pretrained(DEFAULT_MODEL_PATH)
        tokenizer = AutoTokenizer.from_pretrained(model_name)

        # handle multiple steps internally, like tokenizing, feeding tokens into model, and processing the output into a human-readble form
        pipeline = transformers.pipeline(
            "text-generation",
            model=model_name,
            tokenizer=tokenizer,
            trust_remote_code=True,
            device_map="auto",
        )

        return pipeline, tokenizer

    def generate_answer(self, prompt):
        # generating responses
        sequences = self.pipeline(
            prompt,
            max_length=500,
            do_sample=True,
            top_k=10,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )

        # extracting and return the generated text
        return sequences


ai_model: ModelPipeline = ModelPipeline()
