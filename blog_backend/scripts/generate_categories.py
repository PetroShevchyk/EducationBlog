import django
import os
import sys

from collections import Counter


sys.path.append(os.path.join(os.path.abspath(os.path.dirname(__file__)), '..'))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_backend.settings")
django.setup()


from post.models import Post, Categories

def extract_hashtag(text, categories):
    for word in text.split():
        if word[0] == '#':
            categories.append(word[1:])
    
    return categories

def categories_update():
    for category in Categories.objects.all():
        category.delete()

    categories = []

    for post in Post.objects.all():
        extract_hashtag(post.body, categories)

    for category in Counter(categories).most_common(10):
        Categories.objects.create(hashtag=category[0], occurences=category[1])
