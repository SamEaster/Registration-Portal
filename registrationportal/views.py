from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from competitions.models import Competition,Module
from users.models import NewUser
# Create your views here.

def home(request):
    user = NewUser.objects.filter(email=request.user).first()
    if user:
        if not user.fullname or not user.phone_number:
            user.delete()
            messages.error(request, "Your profile is incomplete. Please log in again and complete your profile.")
            return redirect('/')
    competitions = Competition.objects.all()
    modules = Module.objects.all()
    module_competition_counts = {module.id: Competition.objects.filter(module=module).count() for module in modules}
    for module in modules:
        module.competition_count = module_competition_counts[module.id]
    return render(request, 'home/index.html', {'competitions': competitions, 'modules': modules, 'module_competition_counts': module_competition_counts})
def sponsor(request):
    return render(request, 'sponsor/sponsor.html')

@login_required(login_url='login')
def rulebook(request):
    return render(request, 'rules.html',{'active_page':'rulebook'})
  
@login_required(login_url='login')
def contact(request):
    return render(request, 'contactus.html',{'active_page':'contact'})