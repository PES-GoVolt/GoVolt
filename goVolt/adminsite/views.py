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
def save_user_data(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        uid = request.GET.get('uid')
        edit_user_with_uid(uid,first_name,last_name)
    response_data = {'status': 'success', 'message': 'Data Saved.'}
    return JsonResponse(response_data)
def route_delete_post(request):
    if request.method == 'POST':
        id = request.GET.get('route_id')
        delete_route(id)
    response_data = {'status': 'success', 'message': 'Route deleted.'}
    return JsonResponse(response_data)    
def charger_delete_post(request):
    if request.method == 'POST':
        id = request.GET.get('charger_id')
        delete_charger(id)
    response_data = {'status': 'success', 'message': 'Charger deleted.'}
    return JsonResponse(response_data)

def bikestation_delete_post(request):
    if request.method == 'POST':
        id = request.GET.get('station_id')
        delete_bikestation(id)
    response_data = {'status': 'success', 'message': 'Bikestation deleted.'}
    return JsonResponse(response_data)

def admin_edit_user_view(request):
    uid = request.GET.get('uid')
    user = get_user_info_by_uid(uid)
    return render(request,'editUser.html',{'user':user})

def admin_users_view(request):

    users = get_all_users()

    return render(request,'adminUsers.html',{'users':users})

def admin_chats_view(request):

    chats = get_all_chats()

    return render(request,'adminChats.html',{'chats':chats})

def admin_routes_view(request):
    routes = get_all_routes_admin()
    return render(request,'adminRoutes.html',{'routes':routes})
def admin_messages_view(request):

    messages = get_all_messages()
    print(messages)
    return render(request,'adminMessages.html',{'messages':messages})

def admin_chargers_view(request):

    chargers = get_all_chargers()

    return render(request,'adminChargers.html',{'chargers':chargers})


def admin_bikestations_view(request):

    stations = get_all_bikestations()

    return render(request,'adminBikestations.html',{'stations':stations})