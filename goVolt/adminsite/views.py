from django.shortcuts import render


from api.users.services import get_all_users,get_user_info_by_uid,edit_user_with_uid
from api.chats.services import get_all_chats,get_all_messages
from api.chargers.services import get_all_chargers
from api.bikestations.services import get_all_bikestations
from api.routes.services import get_all_routes_admin
from django.http import JsonResponse
from api.chargers.services import delete_charger
from api.bikestations.services import delete_bikestation
from api.routes.services import delete_route
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

def admin_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username)
        print(password)
        user = authenticate(username=username, password=password)

        if user is not None and user.is_superuser:
            login(request, user)
            return redirect('admin-users-view')
        else:
            return render(request, 'adminLogin.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'adminLogin.html')

def save_user_data(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_superuser:
            first_name = request.POST.get('firstName')
            last_name = request.POST.get('lastName')
            uid = request.GET.get('uid')
            edit_user_with_uid(uid,first_name,last_name)
            response_data = {'status': 'success', 'message': 'Data Saved.'}
            return JsonResponse(response_data)
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')
    
def route_delete_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_superuser:
            id = request.GET.get('route_id')
            delete_route(id)

            response_data = {'status': 'success', 'message': 'Route deleted.'}
            return JsonResponse(response_data)
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')
     
def charger_delete_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_superuser:
            id = request.GET.get('charger_id')
            delete_charger(id)

            response_data = {'status': 'success', 'message': 'Charger deleted.'}
            return JsonResponse(response_data)
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')


def bikestation_delete_post(request):
    if request.method == 'POST' and request.user.is_authenticated:
        if request.user.is_superuser:
            id = request.GET.get('station_id')
            delete_bikestation(id)

            response_data = {'status': 'success', 'message': 'Bikestation deleted.'}
            return JsonResponse(response_data)
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')

def admin_edit_user_view(request):
    uid = request.GET.get('uid')
    user = get_user_info_by_uid(uid)
    return render(request, 'editUser.html', {'user': user})

def admin_users_view(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            users = get_all_users()
            return render(request, 'adminUsers.html', {'users': users})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')

def admin_chats_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            chats = get_all_chats()
            return render(request, 'adminChats.html', {'chats': chats})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')

def admin_routes_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            routes = get_all_routes_admin()
            return render(request, 'adminRoutes.html', {'routes': routes})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')

def admin_messages_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            messages = get_all_messages()
            print(messages)
            return render(request, 'adminMessages.html', {'messages': messages})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')

def admin_chargers_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            chargers = get_all_chargers()
            return render(request, 'adminChargers.html', {'chargers': chargers})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')


def admin_bikestations_view(request):

    if request.user.is_authenticated:
        if request.user.is_superuser:
            stations = get_all_bikestations()
            return render(request, 'adminBikestations.html', {'stations': stations})
        else:
            return redirect('admin-login')
    else:
        return redirect('admin-login')