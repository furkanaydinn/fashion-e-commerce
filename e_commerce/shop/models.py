from django.db import models
from django.db.models import Avg, Count
from django.contrib.auth.models import User
from django.utils import timezone

from ckeditor_uploader.fields import RichTextUploadingField

# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=50)
    slug = models.SlugField(null=False, unique=True)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/' % self.slug
    
    def toJSON(self):
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'created_at': timezone.localtime(self.created_at).strftime('%Y-%m-%d %H:%M:%S'),
            'updated_at': timezone.localtime(self.updated_at).strftime('%Y-%m-%d %H:%M:%S')
        }

    

class Product(models.Model):

    STATUS_CHOICES = (
        ('Draft', 'Draft'),
        ('Waiting approval', 'Waiting approval'),
        ('ACTIVE', 'ACTIVE'),
        ('Deleted', 'Deleted'),
    )

    category = models.ForeignKey(Category, related_name='product_categories', on_delete=models.CASCADE)
    image=models.ImageField(upload_to='product_images/',null=False)
    title = models.CharField(max_length = 150)
    tags = models.CharField(max_length=100)
    sku = models.CharField(max_length=50)
    brand = models.CharField(max_length=50,null=True)
    intro = models.CharField(max_length=200,null=True)
    description = RichTextUploadingField()
    price = models.DecimalField(max_digits=12, decimal_places=2,default=0)
    amount=models.IntegerField(default=0)
    slug = models.SlugField(null=False, unique=True)
    status=models.CharField(max_length=40,choices=STATUS_CHOICES, default='Active')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return '/%s/%s/' % (self.category.slug, self.slug)

    
    def avaregereview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(avarage=Avg('rate'))
        avg=0
        if reviews["avarage"] is not None:
            avg=float(reviews["avarage"])
        return avg

    def countreview(self):
        reviews = Comment.objects.filter(product=self, status='True').aggregate(count=Count('id'))
        cnt=0
        if reviews["count"] is not None:
            cnt = int(reviews["count"])
        return cnt
    


class Comment(models.Model):
    STATUS = (
        ('New', 'New'),
        ('True', 'True'),
        ('False', 'False'),
    )

    product=models.ForeignKey(Product,on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=50, blank=True)
    comment = models.CharField(max_length=250,blank=True)
    rate = models.IntegerField(default=1)
    status=models.CharField(max_length=10,choices=STATUS, default='New')
    create_at=models.DateTimeField(auto_now_add=True)
    update_at=models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.subject
