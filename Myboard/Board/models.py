from django.db import models
from django.contrib.auth.models import User
from markdown import markdown
from django.utils.html import mark_safe
import math


class Board(models.Model):
	name = models.CharField(max_length = 30, unique = True)
	description = models.CharField(max_length = 140)
	views = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.name

	def get_posts_count(self):
		return Post.objects.filter(topic__board = self).count()

	def get_last_post(self):
		return Post.objects.filter(topic__board=self).order_by('-created_at').first()

		 

class Topic(models.Model):
	subject = models.CharField(max_length = 260)
	last_updated = models.DateTimeField(auto_now_add = True)
	board = models.ForeignKey(Board, related_name = 'topics')
	starter = models.ForeignKey(User, related_name = 'topics')
	views = models.PositiveIntegerField(default = 0)
	def __str__(self):
		return self.subject	


	def get_page_count(self):
		count = self.posts.count()
		pages = count / 10
		return math.ceil(pages)
	def has_many_pages(self, count=None):
		if count is None:
			count = self.get_page_count()
			return count > 6
	def get_page_range(self):
		count = self.get_page_count()
		if self.has_many_pages(count):
			return range(1, 5)
		return range(1, count + 1)

class Post(models.Model):
	topic = models.ForeignKey(Topic, related_name = 'posts')
	message = models.TextField(max_length = 4000)
	created_at = models.DateTimeField(auto_now_add = True)
	created_by = models.ForeignKey(User, related_name = 'posts')
	updated_at = models.DateTimeField(null = True)
	updated_by = models.ForeignKey(User,null = True, related_name = '+')

	def __str__(self):
		return self.message[:50]

	def get_message_markdown(self):
		return mark_safe(markdown(self.message, safe_mode = 'escap' ))
# Create your models here.
