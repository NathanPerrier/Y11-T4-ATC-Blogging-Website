import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from joblib import Parallel, delayed

#* # Sample data
# blogs = pd.DataFrame({
#     'Blog_ID': [1, 2, 3, 4, 5, ...],  # Include all 50 blogs
#     'Title': ['Blog 1', 'Blog 2', 'Blog 3', 'Blog 4', 'Blog 5', ...],  # Include titles
#     'Content': ['Content of Blog 1', 'Content of Blog 2', 'Content of Blog 3', 'Content of Blog 4', 'Content of Blog 5', ...],
#     'Tags': ['Tech', 'Travel', 'Tech', 'Food', 'Travel', ...]  # Include tags
# })

# users = pd.DataFrame({
#     'User_ID': [101, 102, 103],
#     'Name': ['User A', 'User B', 'User C'],
#     'Interests': [['Tech', 'Travel'], ['Food'], ['Tech']]
# })

class BlogRecommendations:
    def __init__(self, blogs, users):
        self.blogs = blogs
        self.users = users
        self.tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(self.blogs['Content'])

    # Calculate cosine similarity between blogs in parallel
    def calculate_cosine_similarity(self, user_tfidf):
        return linear_kernel(user_tfidf, self.tfidf_matrix).flatten()

    # Recommendation function
    def recommend(self, user_id, num_recommendations=5):
        try:
            user = self.users[self.users['User_ID'] == user_id]  #change to match database #* user = user.id
            user_interests = user['Interests'].values[0]

            # Calculate the TF-IDF vectors for user interests
            user_tfidf = self.tfidf_vectorizer.transform([' '.join(user_interests)])

            # Calculate cosine similarity for all blogs in parallel
            similarities = Parallel(n_jobs=-1)(delayed(self.calculate_cosine_similarity)(user_tfidf) for _ in range(len(self.blogs)))

            # Get top blog indices with highest similarity
            blog_indices = sorted(range(len(similarities)), key=lambda i: similarities[i], reverse=True)[:num_recommendations]

            # Extract recommended blogs
            recommended_blogs = [
                (self.blogs.iloc[index]['Blog_ID'], self.blogs.iloc[index]['Title'], self.blogs.iloc[index]['Tags'], similarities[index])
                for index in blog_indices
            ]

            return recommended_blogs

        except IndexError:
            return "User not found or interests not specified."
