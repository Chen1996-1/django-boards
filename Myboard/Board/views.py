from django.core.urlresolvers import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.models import User
from .models import Board, Post, Topic 
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Count
#===============GCBV================
from django.views.generic import UpdateView
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.generic import ListView
import math
class BoardListView(ListView):
	model = Board
	context_object_name = 'boards'
	template_name = 'home.html' 

class PostUpdateView(UpdateView):
	model = Post
	fields = ('message',)
	template_name = 'edit_post.html'
	pk_url_kwarg = 'post_pk'
	context_object_name = 'post'
	def get_queryset(self):
		queryset = super().get_queryset()
		return queryset.filter(created_by =self.request.user)
	def form_valid(self,form):
		post = form.save(commit = False)
		post.updated_by = self.request.user
		post.updated_at = timezone.now()
		post.save()
		return redirect('topic_posts', pk=post.topic.board.pk, topic_pk = post.topic.pk)


class TopicListView(ListView):
	model = Topic
	context_object_name =  'topics'
	template_name = 'board_topics.html'
	paginate_by = 10
	def get_context_data(self, **kwargs):

		session_key = 'viewed_board_{}'.format(self.board.pk)
		if not self.request.session.get(session_key, False):
			self.board.views += 1
			self.board.save()
			self.request.session[session_key] = True

		kwargs['board'] = self.board
		return super().get_context_data(**kwargs)

	def get_queryset(self):
		self.board = get_object_or_404(Board, pk=self.kwargs.get('pk'))
		queryset = self.board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
		return queryset

# def topic_posts(request, pk, topic_pk):
# 	topic = get_object_or_404(Topic, board__pk = pk, pk = topic_pk)
# 	topic.views += 1
# 	topic.save()
# 	return render(request, 'topic_posts.html', {'topic':topic})
class PostListView(ListView):
	model = Post
	context_object_name = 'posts'
	template_name = 'topic_posts.html'
	paginate_by = 4
	def get_context_data(self, **kwargs):
		# self.topic.views += 1
		# self.topic.save()
		
		session_key = 'viewed_topic_{}'.format(self.topic.pk)
		if not self.request.session.get(session_key, False):
			self.topic.views += 1
			self.topic.save()
			self.request.session[session_key] = True

		kwargs['topic'] = self.topic
		return super().get_context_data(**kwargs)
	def get_queryset(self):
		self.topic = get_object_or_404(Topic, board__pk=self.
		kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
		queryset = self.topic.posts.order_by('created_at')
		return queryset

@login_required
def new_topic(request, pk):
	board = get_object_or_404(Board, pk=pk)
	user = request.user                               # TODO: get the currently logged in user
	if request.method == 'POST':
		form = NewTopicForm(request.POST)
		if form.is_valid():
			topic = form.save(commit=False)
			topic.board = board
			topic.starter = user
			topic.save()

			post = Post.objects.create(
				message=form.cleaned_data.get('message'),
				topic=topic,
				created_by=user
			)
			return redirect('board_topics', pk = pk, )
	else:
		form = NewTopicForm()
	return render(request, 'new_topic.html', {'board': board, 'form': form})

@login_required
def reply_topic(request,pk, topic_pk):
	topic = get_object_or_404(Topic, board__pk=pk, pk = topic_pk)
	if request.method == 'POST':
		form = PostForm(request.POST)
		if form.is_valid():
			post = form.save(commit = False)
			post.topic = topic
			post.created_by = request.user
			post.save()
			topic.last_updated = timezone.now()
			topic.save()

			topic_url = reverse('topic_posts', kwargs={'pk':pk, 'topic_pk': topic_pk})
			topic_post_url = '{url}?page={page}'.format(url=topic_url,id=post.pk,page=math.ceil(topic.posts.count()/4))
			return redirect(topic_post_url)


			
	else:
		form = PostForm()
	return render(request, 'reply_topic.html', {'topic':topic, 'form':form})


