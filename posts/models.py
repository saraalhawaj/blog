from django.db import models
from django.core.urlresolvers import reverse
from django.db.models.signals import pre_save
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from django.dispatch import receiver
# Create your models here.
class PostHome(models.Model):
	title = models.CharField(max_length=250)
	author = models.ForeignKey(User, default=1)
	slug = models.SlugField(unique=True)
	content = models.TextField()
	draft = models.BooleanField(default=False)
	publish_date =models.DateField()
	timestamp = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(null=True, blank=True, upload_to="post_images")

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse("detail", kwargs={"post_slug":self.slug})


	class Meta:
		ordering = ['title']

def create_slug(instance, new_slug=None): 
    slug = slugify (instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = PostHome.objects.filter(slug=slug).order_by("-id")
    exists = qs.exists()
    if exists:
        new_slug = "%s-%s"%(slug,qs.first().id)
        return create_slug(instance, new_slug=new_slug)
    return slug


# @receiver(pre_save, sender=PostHome)
def pre_save_post_reciever(sender, instance, *args, **kwargs):
    instance.slug=slugify(instance.title)

pre_save.connect(pre_save_post_reciever,sender=PostHome)



class Like(models.Model):
	user = models.ForeignKey(User)
	post = models.ForeignKey(PostHome)
	timestamp = models.DateTimeField(auto_now_add=True)