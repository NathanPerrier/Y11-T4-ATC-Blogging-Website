from backend.config import *
from backend.tests.db import db, app
from backend.blog.comments import Comments

class TestCommentsModel(unittest.TestCase):

    def test_comments_attributes(self):
        # Checkpoint: Testing attributes of Comments class
        comment = Comments()
        self.assertTrue(hasattr(comment, 'id'), "Attribute 'id' not found")
        self.assertTrue(hasattr(comment, 'user_id'), "Attribute 'user_id' not found")
        self.assertTrue(hasattr(comment, 'blog_id'), "Attribute 'blog_id' not found")
        self.assertTrue(hasattr(comment, 'comment'), "Attribute 'comment' not found")
        # Add more attributes
