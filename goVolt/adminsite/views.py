from django.shortcuts import render


from api.users.services import get_all_users,get_user_info_by_uid,edit_user_with_uid
from api.chats.services import get_all_chats,get_all_messages
from django.http import JsonResponse



def save_user_data(request):
    if request.method == 'POST':
        first_name = request.POST.get('firstName')
        last_name = request.POST.get('lastName')
        uid = request.GET.get('uid')
        edit_user_with_uid(uid,first_name,last_name)
    response_data = {'status': 'success', 'message': 'Data Saved.'}
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

def admin_messages_view(request):

    messages = get_all_messages()
    print(messages)
    return render(request,'adminMessages.html',{'messages':messages})

def admin_chargers_and_bikestations_view(request):

    users = get_all_users()

    return render(request,'adminUsers.html',{'users':users})