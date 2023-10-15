from backend.config import *
from backend.tests.db import db, app
from backend.blog.blog import Blog

class TestBlogModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Class-level setup, e.g., creating test database
        pass

    @classmethod
    def tearDownClass(cls):
        # Class-level teardown, e.g., deleting test database
        pass

    def setUp(self):
        # Setup code here, like database initialization or mocking
        with app.app_context():
            self.blog = Blog(id=1, title="Test Blog", content="This is a test blog.", user_id=1)
            db.session.add(self.blog)
            db.session.commit()
        
    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_attributes(self):
        # Checkpoint: Testing attributes of Blog class
        self.assertTrue(hasattr(self.blog, 'id'), "Attribute 'id' not found")
        self.assertTrue(hasattr(self.blog, 'title'), "Attribute 'title' not found")
        self.assertTrue(hasattr(self.blog, 'content'), "Attribute 'content' not found")
        self.assertTrue(hasattr(self.blog, 'user_id'), "Attribute 'user_id' not found")

    def test_save(self):
        # Checkpoint: Testing save method
        with app.app_context():
            blog = Blog(id=2, title="Another Test Blog", content="This is another test blog.", user_id=1)
            db.session.add(blog)
            db.session.commit()
        self.assertIsNotNone(Blog.get_by_id(2))

    def test_delete(self):
        # Checkpoint: Testing delete method
        with app.app_context():
            blog = Blog.get_by_id(1)
            db.session.remove(blog)
            db.session.commit()
        self.assertIsNone(Blog.get_by_id(1))

    # @patch('your_project.some_dependency')
    # def test_some_method_with_dependency(self, mock_dependency):
    #     # Checkpoint: Testing methods that have external dependencies
    #     mock_dependency.some_function.return_value = "Mocked value"
    #     result = self.blog.some_method()
    #     self.assertEqual(result, "Expected value based on mock")

    # def test_error_cases(self):
    #     # Checkpoint: Testing error handling
    #     with self.assertRaises(SomeException):
    #         self.blog.some_error_prone_method()