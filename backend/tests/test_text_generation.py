import unittest
from backend.ai.text_generation_model.main import generate_text

class TestAI(unittest.TestCase):
    def test_generate_text(self):
        text = generate_text('Hello, world!')
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)

    def test_generate_text_with_params(self):
        text = generate_text('Hello, world!', model_params={'n_ctx': 10}, encoder_params={'n_vocab': 10}, sampling_params={'temperature': 0.5})
        self.assertIsInstance(text, str)
        self.assertGreater(len(text), 0)