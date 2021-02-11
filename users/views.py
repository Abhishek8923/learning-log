from django.shortcuts import render,redirect
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
def register(request):
    """to register new users"""
    if request.method != 'POST':
        form=UserCreationForm()
    else:
        form=UserCreationForm(data=request.POST)
        if form.is_valid():
            new_user=form.save()
            #login the new user
            login(request,new_user)
            return redirect('learning_logs:index')

    #to display blank and invalid form
    context={'form':form}
    return render(request,'registration/register.html',context)            