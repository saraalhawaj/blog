from django.shortcuts import render, get_object_or_404, redirect
from .models import PostHome, Like
from .forms import PostForm, UserSignUp, UserLogin
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, JsonResponse
from django.utils import timezone
from django.db.models import Q
from urllib.parse import quote
from django.contrib.auth import login, logout, authenticate




def usersignup(request):
	context = {}
	form = UserSignUp()
	context['form'] = form

	if request.method == "POST":
		form = UserSignUp(request.POST)
		if form.is_valid():
			user = form.save()
			x = user.username
			y = user.password


			user.set_password(y)
			user.save()


			auth = authenticate(username=x, password=y)
			login(request, auth)


			return redirect("list")
		messages.warning(request, form.errors)
		return redirect("signup")
	return render(request, 'signup.html', context)


def userlogin(request):
	context ={}
	form = UserLogin()
	context['form'] = form


	if request.method == "POST":
		form = UserLogin(request.POST or None)
		if form.is_valid():
			some_username = form.cleaned_data['username']
			some_password = form.cleaned_data['password']

			auth = authenticate(username=some_username, password=some_password)
			if auth is not None:
				login(request, auth)
				return redirect("list")
			messages.warning(request, 'incorect username/Password combination')
			return redirect("login")
		messages.warning(request,form.errors)
		return redirect("login")
	return render(request, 'login.html',context)


def userlogout(request):
	logout(request)
	return redirect("login")



def some_function(request):
	some_dictionary = {
	"some_key": "with a random value"
	}
	return render(request, 'M.html', context)




def post_list(request):
	today = timezone.now().date()


	objects = PostHome.objects.filter(draft=False, publish_date__lte=today)
	if request.user.is_staff:
		objects = PostHome.objects.all()


	query = request.GET.get('q')
	if query:
		objects = objects.filter(
			Q(title__icontains=query)|
			Q(content__icontains=query)|
			Q(author__first_name__icontains=query)|
			Q(author__last_name__icontains=query)
			).distinct()


	# objects = PostHome.objects.all().order_by('titlr, 'id')
	paginator = Paginator(objects, 5)
	number = request.GET.get('page')

	try:
		objects = paginator.page(number)

	except PageNotAnInteger:
	   
		objects = paginator.page(1)
	except EmptyPage:
		
		objects = paginator.page(paginator.num_pages)

	context = {
	"post_items": objects,
	"today": today,
	}

	return render(request, "List.html", context)


def post_detail(request, post_slug):
	#item=PostHome.objects.get(id=1000)
	today = timezone.now().date()
	item = get_object_or_404(PostHome, slug= post_slug)
	if not request.user.is_authenticated(): 
		if item.draft or item.publish_date > today:
			raise Http404

	if request.user.is_authenticated():
		if Like.objects.filter(post=item, user=request.user).exists():
			like = True
		else:
			like = False

	like_count = item.like_set.count()



	context = {
	"item": item,
	"share_string": quote(item.content),
	"like": like,
	"like_count": like_count,
	}

	return render(request, "detail.html", context)

def post_create(request):
	if not request.user.is_staff:
		raise Http404
	form = PostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		sara_post = form.save(commit=False)
		sara_post.author = request.user
		sara_post.save()
		messages.success(request, "you just added a text")
		return redirect("list")
	context = {
		"form":form,
	}
	return render (request, "post_create.html", context)

def post_update(request, post_slug):
	item = PostHome.objects.get(slug=post_slug)
	form = PostForm(request.POST or None, request.FILES or None, instance=item)
	if form.is_valid():
		form.save()
		messages.info(request, "you changed something")
		return redirect("list")

	context = {
		"form":form,
		"item":item, 
	}
	return render (request, "post_updates.html", context)


def post_delete(request, post_slug):
	PostHome.objects.get(slug=post_slug).delete()
	messages.warning(request, "noooooo")

	return redirect("list")


def like_button(request, post_id):
	post_object = PostHome.objects.get(id=post_id)

	like, created = Like.objects.get_or_create(user=request.user, post= post_object)

	if created:
		action = "like"
	else:
		like.delete()
		action = "unlike"

	like_count = post_object.like_set.count()


	response = { 

			"like_count": like_count,
			"action": action,

	}

	return JsonResponse(response, safe=False)