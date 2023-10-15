from backend.config import *
from backend.tests.db import db, app
from backend.authentication.reset_code import ResetCode

class TestResetCodeModel(unittest.TestCase):

    def test_reset_code_attributes(self):
        # Checkpoint: Testing attributes of ResetCode class
        reset_code = ResetCode()
        self.assertTrue(hasattr(reset_code, 'id'), "Attribute 'id' not found")
        self.assertTrue(hasattr(reset_code, 'user_id'), "Attribute 'user_id' not found")
        self.assertTrue(hasattr(reset_code, 'reset_code'), "Attribute 'reset_code' not found")
        # Add more attributes