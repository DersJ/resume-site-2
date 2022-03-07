from django.test import TestCase
from blog.models import *

class BlogWithArticlesTestCase(TestCase):
    def setUp(self):
        Post.objects.create(title="Post 1 - normal", displayPath="Post 1", subtitle="Post 1 subtitle", public=True, content="Post 1 content")
        Post.objects.create(title="Post 2 - markdown", displayPath="Post 2", subtitle="Post 2 subtitle", public=True, isMarkdownContent=True, content="#Post 2 content")

    def test_blog_post_created(self):
        """Animals that can speak are correctly identified"""
        post = Post.objects.get(title="Post 1 - normal")
        self.assertEqual(post.content, "Post 1 content")
    
    def test_blog_homepage_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 2 - markdown')
    
    def test_blog_list_page_loads(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Post 1 - normal')