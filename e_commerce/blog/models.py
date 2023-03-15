from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.

class Blog(models.Model):

    ACTIVE = 'active'
    DRAFT = 'draft'

    CHOICES_STATUS = (
        (ACTIVE, 'Active'),
        (DRAFT, 'Draft')
    )

    author_name = models.CharField(max_length=30)
    title = models.CharField(max_length=200)  #yazı başlığı
    slug = models.SlugField()  #yazı url
    intro = RichTextUploadingField()  # yazı içerik
    status = models.CharField(max_length=10, choices=CHOICES_STATUS, default=ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)
    post_image = models.ImageField(upload_to = 'blogs/', blank = True, null = True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title


    def get_absolute_url(self):
        return '/%s/' % (self.slug)
    

class Comment(models.Model):
    post = models.ForeignKey(Blog,related_name='comments',on_delete= models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=20)
    comment = models.TextField()

    def __str__(self):
        return self.name
