import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import UserDetails
from django.contrib import messages
from django.http import JsonResponse


# Create your views here.
def hello(request):
    return HttpResponse("Hello World")


def signup(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if UserDetails.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
        else:
            user = UserDetails.objects.create(username=username, email=email, password=password)
            user.save()
            return redirect('login')
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = UserDetails.objects.get(email=email)
            if user.password == password:
                return render(request, 'success.html')
            else:
                messages.error(request, 'Invalid password')
        except UserDetails.DoesNotExist:
            messages.error(request, 'User not found')

    return render(request, 'login.html')


@csrf_exempt
def get_all_users(request):
    users = UserDetails.objects.all()
    user_list = [user.to_dict() for user in users]
    return HttpResponse(json.dumps({'users': user_list}), status=200)


@csrf_exempt
def get_user_by_email(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        return HttpResponse(json.dumps({'user': user.to_dict()}), status=200)
    except UserDetails.DoesNotExist:
        return HttpResponse('User not found', status=404)


@csrf_exempt
def update_user(request, email):
    try:
        user = UserDetails.objects.get(email=email)
        if request.method == 'POST':
            req_body = json.loads(request.body)
            user.username = req_body.get('username', user.username)
            user.password = req_body.get('password', user.password)
            user.save()
        return HttpResponse('User updated successfully', status=200)
    except UserDetails.DoesNotExist:
        return HttpResponse('User not found', status=404)


@csrf_exempt
def delete_user(request, email):
    if request.method == 'DELETE':
        user = get_object_or_404(UserDetails, email=email)
        user.delete()
        return HttpResponse(json.dumps({'message': 'User deleted successfully'}), status=200)
    return HttpResponse("Invalid request method. Only DELETE allowed.", status=500)


@csrf_exempt
def create_user_postman(request):
    if request.method == "POST":
        req_body = json.loads(request.body)
        username = req_body.get('username', '')
        email = req_body.get('email', '')
        password = req_body.get('password', '')

        if UserDetails.objects.filter(email=email).exists():
            return HttpResponse(json.dumps({'message': 'Email already exists'}), status=500)
        else:
            user = UserDetails.objects.create(username=username, email=email, password=password)
            user.save()
            return HttpResponse(json.dumps({'message': 'User created successfully'}), status=200)