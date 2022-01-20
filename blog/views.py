from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.core.paginator import Paginator, EmptyPage,PageNotAnInteger
from django.core.mail import send_mail
from .models import Blog, Comments
from .forms import EmailPostForm, CommentForm
# Create your views here.
"""Functional Views"""
def post_list(request):
	object_list = Blog.objects.all()
	paginator = Paginator(object_list, 3) # 3 posts in each page
	page = request.GET.get('page')
	try:
		posts = paginator.page(page)
	except PageNotAnInteger:
		# If page is not an integer deliver the first page
		posts = paginator.page(1)
	except EmptyPage:
		# If page is out of range deliver last page of results
		posts = paginator.page(paginator.num_pages)
	return render(request,'blog/post/list.html',{'page': page,'posts': posts})
"""Class Based Views"""
# from django.views.generic import ListView
# class PostListView(ListView):
# 	model = Blog
# 	context_object_name = 'posts'
# 	template_name = 'blog/post/list.html'
# 	paginate_by = 2


# 	# return render(request,'blog/post/list.html',{'posts': posts})
def post_detail(request, year, month, day, post):
	post = get_object_or_404(Blog, slug=post,status='published',publish__year=year,publish__month=month,publish__day=day)
	return render(request,'blog/post/detail.html',{'post': post})

def post_share(request, post_id):
# Retrieve post by id
	post = get_object_or_404(Blog, id=post_id, status='published')
	sent = False
	if request.method == 'POST':
# Form was submitted
		form = EmailPostForm(request.POST)
		if form.is_valid():
# Form fields passed validation
			cd = form.cleaned_data
# ... send email
			post_url = request.build_absolute_uri(post.get_absolute_url())
			subject = f"{cd['name']} recommends you read " f"{post.title}"
			message = f"Read {post.title} at {post_url}\n\n" f"{cd['name']}\'s comments: {cd['comments']}"
			send_mail(subject, message, 'jesso1908joy@gmail.com',[cd['to']])
			sent = True
	else:
		form = EmailPostForm()
	return render(request, 'blog/post/share.html', {'post': post,'form': form,'sent':sent})

