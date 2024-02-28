from backend.ai.text_generation_model.model import *
from backend.ai.text_generation_model.encoder import *
from backend.ai.text_generation_model.sample import *

def generate_text(input_text, model_params={}, encoder_params={}, sampling_params={}):
    # Initialize Encoder for encoding and decoding
    encoder = Encoder(**encoder_params)

    # Encoding the input text
    encoded_input = encoder.encode(input_text)

    # Generate text tokens using functionalities from model.py
    output_tokens = model.model(encoded_input, **model_params)

    # Generate text using sample_sequence from sample.py
    generated_tokens = sample_sequence(hparams=sample_params, length=len(output_tokens), context=output_tokens)

    # Decoding the generated tokens to text
    generated_text = encoder.decode(generated_tokens)

    return generated_text
