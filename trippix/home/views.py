from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from .models import User, Post
from .forms import RegistrationForm, SearchForm
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie



@ensure_csrf_cookie
def user_logout(request):
    """
    Представление для выхода пользователя из системы.
    """
    logout(request)  # Метод logout() завершает текущий сеанс пользователя

    # Возвращаем JSON-ответ с сообщением об успешном выходе
    return JsonResponse({'message': 'User logged out successfully'})


@ensure_csrf_cookie
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()  # Создание нового пользователя в базе данных
            return redirect('login')  # Перенаправление на главную страницу после успешной регистрации
    else:
        form = RegistrationForm()  # Создание пустой формы для отображения

    return render(request, 'page3.html', {'form': form})


@ensure_csrf_cookie
def entry(request):
    if request.method == 'POST':
        login_value = request.POST.get('login')
        password = request.POST.get('password')

        print(login_value, password)

        # acces = User.objects.filter(logging = login_value, password = password).last()
        # acces2 = User.objects.filter(logging = login_value, password = password)

        user = authenticate(request, username=login_value, password=password)

        if user != None:
            request.session["username"] = login_value

            return redirect('home')
            login(request, user)
        else:
            try:
                user = User.objects.get(logging=login_value)
                if user.password == password:
                    login(request, user)
                    return redirect('home')
                else:
                    return render(request, 'page2.html', {'error': 'Неправильный логин или пароль'})
            except User.DoesNotExist:
                error_message = f'Пользователь с логином "{login_value}" не найден'
                print(error_message)
                return render(request, 'page2.html', {'error': 'Пользователь не найден'})
            except Exception as e:
                error_message = f'Произошла ошибка: {repr(e)}'
                print(error_message)
                return HttpResponse(error_message)
        login(request, user)

    return render(request, 'page2.html')


def index(request):
    posts = Post.objects.all()
    form = SearchForm(request.GET or None)
    if form.is_valid():
        query = form.cleaned_data['query']
        posts = Post.objects.filter(title__icontains=query)
    return render(request, 'page1.html', {'posts': posts, 'form': form})


@login_required
def userpage(request):
    # Получаем текущего пользователя
    user = request.user
    # Получаем имя пользователя
    username = user.logging
    # Получаем все посты, отсортированные по дате создания
    user_posts = Post.objects.filter(author=user).order_by('created_at')

    context = {'user_posts': user_posts, 'username': username}

    return render(request, 'page4.html', context)


@login_required
def add(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        descriptor = request.POST.get('descriptor')
        tegs = request.POST.get('tegs')
        print(request.FILES)
        # Обработка загрузки изображения
        if request.FILES.get('image'):
            image_file = request.FILES['image']
            # Создаем экземпляр модели Post и сохраняем изображение
            post = Post(title=title, descriptor=descriptor, tags=tegs, photo=image_file, author=request.user)
            post.save()
            # post.photo.save(image_file.name, image_file, save=True)  # Сохраняем путь к файлу изображения в модели
            print(post.__dict__, '1')  # вывод в консоль введеные данные post для проверки
            return redirect('home')  # Перенаправление на страницу успешного добавления

        # return redirect('home')  # Перенаправление на страницу успешного добавления
    return render(request, 'page5.html')


@login_required
def post(request, post_id):
    if request.method == 'POST':
        # Удаление поста
        if 'delete' in request.POST:
            post = Post.objects.get(id=post_id)
            if request.user == post.author:
                post.delete()
                return redirect('home')  # Перенаправление на главную страницу после удаления
            else:
                return redirect('home')  # Обработка случая, когда пользователь пытается удалить чужой пост
        # Лайк поста
        elif 'like' in request.POST:
            post = Post.objects.get(id=post_id)
            # Проверка, что пользователь не является автором поста
            if request.user != post.author:
                # Пример обновления количества лайков и сохранения изменений в базе данных
                post.like += 1  # Увеличиваем количество лайков на 1
                post.save()  # Сохраняем изменения в базе данных
                return redirect('home')  # Перенаправление на главную страницу после лайка
            else:
                # Обработка случая, когда автор поста пытается лайкнуть свой пост
                return redirect('home')  # Например, перенаправить на главную страницу
    else:
        # Отображение поста
        post_html = Post.objects.get(id=post_id)
        return render(request, 'page6.html', {'post_html': post_html})

