from django.shortcuts import render,redirect

from .models import Product
from .forms import RegistrationForm
# Create your views here.

from django.contrib.auth.decorators import login_required, permission_required




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



@login_required
def dashboard(request):
    return render(request,'accounts/dashboard.html')

@login_required
@permission_required('accounts.add_product', raise_exception=True)
def create_product(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        price = request.POST.get('price')
        product = Product(name=name, price=price)
        product.save()
        return redirect('dashboard')
    return render(request, 'accounts/create_product.html')


@permission_required('accounts.approve_leave', raise_exception=True)
def leaveAction(request):
    print("approved")
    return render(request,'accounts/leaveAction.html')



def about(request):
    return render(request,'accounts/about.html')




# loginView
# logoutView
