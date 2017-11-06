from django.shortcuts import render, get_object_or_404
from .models import PostHome

def some_function(request):
	some_dictionary= {
	"some_key": "with a random value"
	}
	return render(request, 'M.html', context)



def post_list(request):
	objects = PostHome.objects.all()
	context = {
	"Post_items": objects,
	}

	return render(request, "List.html", context)


def post_detail(request, PostHome_id):
	#item=PostHome.objects.get(id=1000)
	item = get_object_or_404(PostHome, id= PostHome_id)
	context = {
	"item": item,
	}

	return render(request, "detail.html", context)