from django.shortcuts import render, get_object_or_404, redirect
from .models import PostHome
from .forms import PostForm
from django.contrib import messages

def some_function(request):
    some_dictionary= {
    "some_key": "with a random value"
    }
    return render(request, 'M.html', context)



def post_list(request):
    objects = PostHome.objects.all()
    context = {
    "post_items": objects,
    }

    return render(request, "List.html", context)


def post_detail(request, PostHome_id):
    #item=PostHome.objects.get(id=1000)
    item = get_object_or_404(PostHome, id= PostHome_id)
    context = {
    "item": item,
    }

    return render(request, "detail.html", context)

def post_create(request):
    form = PostForm(request.POST or None)
    if form.is_valid():
        form.save()
        messages.success(request, "you just added a text")
        return redirect("list")

    context = {
        "form":form,
    }
    return render (request, "post_create.html", context)

def post_update(request, PostHome_id):
    item = PostHome.objects.get(id=PostHome_id)
    form = PostForm(request.POST or None, instance=item)
    if form.is_valid():
        form.save()
        messages.info(request, "you changed something")
        return redirect("list")

    context = {
        "form":form,
        "item":item, 
    }
    return render (request, "post_updates.html", context)


def post_delete(request, PostHome_id):
    PostHome.objects.get(id=PostHome_id).delete()
    messages.warning(request, "noooooo")

    return redirect("list")