from django.shortcuts import render, get_object_or_404, redirect
from django.http import Http404
from django.contrib.auth.models import User
from .models import Board, Post, Topic 
from .forms import NewTopicForm, PostForm
from django.contrib.auth.decorators import login_required 
from django.db.models import Count

# def home(request):	
	# board = Board.objects.all()
	# return render(request, 'home.html', {'boards':board})

# def board_topics(request, pk):
# 	# try:
# 	# 	board = Board.objects.get(id= pk)
# 	# except Board.DoesNotExist:
# 	# 	raise Http404
# 	board = get_object_or_404(Board,id=pk)
	
	
# 	queryset = board.topics.order_by('-last_updated').annotate(replies = Count('posts')-1)
# 	page = request.GET.get('page',1)
# 	paginator = Paginator(queryset,10)
# 	try :
# 		topics =  Paginator.page(page)
# 	except PageNotAnInteger:
# 		topics = paginator.page(1)
# 	except EmptyPage:
# 		topics = paginator.page(paginator.num_pages)

# 		return render(request, 'board_topics.html', {'board':board, 'topics':topics})

# def topic_posts(request, pk, topic_pk):
# 	topic = get_object_or_404(Topic, board__pk = pk, pk = topic_pk)
# 	topic.views += 1
# 	topic.save()
# 	return render(request, 'topic_posts.html', {'topic':topic})


# def new_topic(request, pk):
# 	board = get_object_or_404(Board, id = pk)
# 	if request.method == 'POST':
# 		subject = request.POST['subject']
# 		message = request.POST['message']
# 		user = User.objects.first()
# 		topic = Topic.objects.create(
# 			subject = subject,
# 			board = board,
# 			starter = user,
# 			)
# 		post = Post.objects.create(
# 			message = message,
# 			topic = topic,
# 			created_by = user,
# 			)
# 		return redirect('board_topics', pk )
# 	return render(request, 'new_topic.html', {'board':board})