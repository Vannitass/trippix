from django.http import HttpResponse
from django.contrib.auth import authenticate, logout, login
from django.shortcuts import render, redirect
from .models import User
from .forms import RegistrationForm
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

        print(login_value,password)

        # acces = User.objects.filter(logging = login_value, password = password).last()
        # acces2 = User.objects.filter(logging = login_value, password = password)

        user = authenticate(request, username = login_value , password = password)


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


    products_data = [
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image.jpg', 'card_image_user': '/static/images/user-image.jpg'},
        {'title': 'A Cool Guide to Japan - Tokyo, Osaka and Kyoto', 'card_image': '/static/images/image_1.jpg', 'card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_2.jpg', 'card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_3.jpg','card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_4.jpg','card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_5.jpg','card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_6.jpg','card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_7.jpg','card_image_user': '/static/images/user-image.jpg'},
        {'title': 'Canadian Rockies, Rocky Mountains, Banff National Park', 'card_image': '/static/images/image_8.jpg','card_image_user': '/static/images/user-image.jpg'},
    ]

        # Другие данные продуктов
    return render(request, 'page1.html', {'products_data': products_data})

@login_required
def userpage(request):
    # print(request.user.is_authenticated)

    # if request.user.is_authenticated:
    # username = "Егор"
    username = request.session.get("username")
    return render(request, 'page4.html', {'username': username})
    # else:
    #     return HttpResponse('Unauthorized', status=401)