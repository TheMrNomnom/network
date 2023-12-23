from django.test import TestCase, Client
from django.urls import reverse
from .models import User, Post
import json


class IndexViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_index_view_get(self):
        response = self.client.get(reverse("index"))
        self.assertEqual(response.status_code, 200)

    def test_index_view_post(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("index"), {"text": "New Post"})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(Post.objects.filter(text="New Post").exists())


class FollowingViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.followed_user = User.objects.create_user(
            username="followeduser", password="12345"
        )
        self.user.following.add(self.followed_user)

    def test_following_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.get(reverse("following"))
        self.assertEqual(response.status_code, 200)


class EditPostViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(creator=self.user, text="Original Text")

    def test_edit_post_successful(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("edit_post"),
            json.dumps({"post_id": self.post.id, "edited_text": "Updated Text"}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.post.refresh_from_db()
        self.assertEqual(self.post.text, "Updated Text")


class ProfilePageViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_profile_page_view(self):
        response = self.client.get(reverse("profile_page", args=[self.user.username]))
        self.assertEqual(response.status_code, 200)


class LikeSystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.post = Post.objects.create(creator=self.user, text="Test Post")

    def test_add_like(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("like_post"),
            json.dumps({"post_id": self.post.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.user in self.post.likes.all())

    def test_remove_like(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("unlike_post"),
            json.dumps({"post_id": self.post.id}),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(self.user in self.post.likes.all())


class FollowSystemTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.other_user = User.objects.create_user(
            username="otheruser", password="12345"
        )

    def test_follow(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("follow", args=[self.other_user.id]))
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertTrue(self.other_user in self.user.following.all())

    def test_unfollow(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(reverse("unfollow", args=[self.other_user.id]))
        self.assertEqual(response.status_code, 302)  # Redirect expected
        self.assertFalse(self.other_user in self.user.following.all())
