from backend.config import *
from backend.tests.db import db, app
from backend.ai.blog_recommendations import BlogRecommendations

class TestBlogRecommendationModel(unittest.TestCase):
    # Sample data
    blogs = pd.DataFrame({
        'Blog_ID': [1, 2, 3, 4, 5],
        'Title': ['Blog 1', 'Blog 2', 'Blog 3', 'Blog 4', 'Blog 5'],
        'Content': ['Tech Content', 'Travel Content', 'Tech and Travel', 'Food Blog', 'Another Travel Blog'],
        'Tags': ['Tech', 'Travel', 'Tech', 'Food', 'Travel']
    })

    users = pd.DataFrame({
        'User_ID': [101],
        'Name': ['User A'],
        'Interests': [['Tech', 'Travel']]
    })

    def setUp(self):
        self.blog_recommender = BlogRecommendations(self.blogs, self.users)

    def test_recommend(self):
        recommended_blogs = self.blog_recommender.recommend(user_id=101, num_recommendations=5)
        self.assertEqual(len(recommended_blogs), 5)
        self.assertListEqual(list(recommended_blogs.columns), ['Blog_ID', 'Title', 'Content', 'Tags'])

    def test_recommend_with_invalid_user_id(self):
        recommended_blogs = self.blog_recommender.recommend(user_id=102, num_recommendations=5)
        self.assertIsNone(recommended_blogs)

    def test_recommend_with_invalid_num_recommendations(self):
        recommended_blogs = self.blog_recommender.recommend(user_id=101, num_recommendations=0)
        self.assertIsNone(recommended_blogs)

    def test_recommend_with_empty_blogs_and_users(self):
        empty_blogs = pd.DataFrame(columns=['Blog_ID', 'Title', 'Content', 'Tags'])
        empty_users = pd.DataFrame(columns=['User_ID', 'Name', 'Interests'])
        empty_blog_recommender = BlogRecommendations(empty_blogs, empty_users)
        recommended_blogs = empty_blog_recommender.recommend(user_id=101, num_recommendations=5)
        self.assertIsNone(recommended_blogs)