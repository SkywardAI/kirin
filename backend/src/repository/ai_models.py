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
        print(prompt)
        print("----------------------")
        sequences = self.pipeline(
            prompt,
            max_length=150,
            truncation=True,
            do_sample=True,
            top_k=1,
            no_repeat_ngram_size=2,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
        )
        # res = self.tokenizer.decode(sequences[0], skip_special_tokens=True)
        res = (
            sequences[0]
            .get("generated_text")
            .replace("string<|endoftext|>", "")
            .replace("<|endoftext|>", "")
            .replace("\n", "")
        )
        print(res)
        # extracting and return the generated text
        return res


ai_model: ModelPipeline = ModelPipeline()
