from django.contrib.auth.models import Group

def get_user_group(request):
    query_set = Group.objects.filter(user = request.user)
    if not query_set:
        query_set = ''
    else:
        query_set = query_set[0].name.capitalize()
        if query_set == 'khách hàng':
            query_set = 'Xin chào'

    return query_set