from django.shortcuts import render, render_to_response, get_object_or_404

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.contrib.auth.models import User
from django.utils import timezone

from bunk.models import Bunk


def index(request):
    """ Show list of num_bunks recent bunks. """
    num_bunks = 10
    user = request.user
    logged_in = user.is_authenticated()

    username = 'Guest! Sign in to send some bunks'
    if logged_in:
        username = user.username

    recent_bunk_list = Bunk.objects.all().order_by('-time')[:num_bunks]
    context = {'recent_bunk_list': recent_bunk_list, 'user': username,
               'logged_in': logged_in}
    return render(request, 'bunk/index.html', context)


@login_required(redirect_field_name='')
def user_detail(request, user_id):
    """ Details for logged in user. """
    user_id = int(user_id)
    view_user = User.objects.get(pk=user_id)
    logged_in = request.user.is_authenticated()

    # get the bunks with this user
    user_bunks = []
    bunks = Bunk.objects.all().order_by('-time')
    for bunk in bunks:
        if (bunk.from_user.id == user_id) or (bunk.to_user.id == user_id):
            user_bunks.append(bunk)

    context = {'user': view_user, 'bunk_list': user_bunks,
               'logged_in': logged_in}
    return render(request, 'bunk/user_detail.html', context)


@login_required(redirect_field_name='')
def bunk_form(request):
    """ Form to bunk someone. """
    user = request.user
    logged_in = user.is_authenticated()

    user_list = []
    for u in User.objects.all():
        if u != user:
            user_list.append(u)

    context = {'user': user, 'user_list': user_list, 'logged_in': logged_in}
    return render(request, 'bunk/bunk_form.html', context)


@login_required(redirect_field_name='')
def bunked(request):
    """ Create the bunk, return the user to the main page. """
    to = request.POST['to']
    if to == 'default':
        return bunk_form(request)

    to_user = get_object_or_404(User, pk=to)

    from_user = request.user
    time = timezone.now()
    new_bunk = Bunk(from_user=from_user, to_user=to_user, time=time)
    new_bunk.save()

    return index(request)


def login_user(request):
    """ Log in a user. Display state of their login attempt. """
    state = "Please log in below..."
    username = password = ''
    logged_in = request.user.is_authenticated()

    if request.POST:
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                state = "You're successfully logged in! Go send some bunks!"
                return index(request)
            else:
                state = "Account is inactive."
        else:
            state = "Your username and/or password were incorrect."

    return render_to_response('bunk/login.html', {'state': state,
                              'username': username, 'logged_in': logged_in},
                              context_instance=RequestContext(request))


def logout_user(request):
    """ Log out the user and send to login page. """
    logout(request)
    return login_user(request)
