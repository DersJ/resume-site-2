from email import message
from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from users.forms import UpdateUserForm


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, 'Your changes have been saved')
    else:
        user_form = UpdateUserForm(instance=request.user)
    return render(request, "account/profile.html", {'user_form': user_form})