from models import Post
from django.contrib.auth.models import User
user = User.objects.get(username='username')  # Замените 'username' на имя пользователя
posts = Post.objects.filter(author=user)
for post in posts:
    print(f'Title: {post.title}')
    print(f'Descriptor: {post.descriptor}')
    print(f'Tags: {post.tags}')
    print('---')

