from django.shortcuts import render,redirect
from .forms import RegistrationForm
# Create your views here.






def home(request):
    return render(request,'accounts/home.html')



def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect('login')

    else:
        form = RegistrationForm()
    return render(request,'accounts/register.html',{'form': form })

# loginView
