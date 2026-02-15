from django.http.response import BadHeaderError
from django.shortcuts import render, redirect, HttpResponse,HttpResponseRedirect, get_object_or_404
from django.template.loader import render_to_string
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from competitions.models import CompTeam, Competition, Module, SubmitPerformance
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
import json
from .forms import AddMemberForm,AddMemberFormSet;
from users.models import Team, TeamMembers,NewUser
from itertools import chain
from django.db.models import Q, Prefetch
from json import dumps
from django.conf import settings
from users.views import create_new_ref_number
# Create your views here.


@login_required(login_url='login')
def showallcompetitions(request):
    # create atleast 1 module bedore runserver
    modulequery = request.GET.get('module') or False
    modulefilter1 = request.GET.get('filter1') or False
    modulefilter2 = request.GET.get('filter2') or False
    compfilter3 = request.GET.get('filter3') or False
    module_comp = Competition.objects.all()
    module1 = Competition.objects.filter(event_name="DID")
    module = False
    if modulequery:
        module = Module.objects.get(
            module_query_name_without_spaces_all_small=modulequery)
        module_comp = module_comp.filter(module=module)
    if (modulefilter1):
        if (modulefilter1 == '0'):
            module_comp = module_comp.filter(~Q(max_members=1))
        else:
            module_comp = module_comp.filter(min_members=1, max_members=1)
    if (modulefilter2):
        module_comp = module_comp.filter(online=modulefilter2)
    if (compfilter3):
        flt3 = compfilter3.replace("+", " ")
        module_comp = module_comp.filter(event_name__icontains=flt3)
    modules = Module.objects.all().reverse()
   
    modulename = ""
    if module:
        modulename = module.module_query_name_without_spaces_all_small

    datajson = list(Competition.objects.all(
    ).values_list('event_name', flat=True))
    for i in datajson:
        print(i)
    # datajson=dumps(module1)
    allModules=Module.objects.all()
 
    return render(request, 'competitions/allcomp.html', {'modules': allModules, 'allcomp': module_comp, 'modulename': modulename, 'active_page': 'competitions', 'data': datajson})

@login_required(login_url='login')
def all_registrations(request):
  allcompetitions = CompTeam.objects.filter(leader=request.user)
  competition_details_list = []
  for detail in allcompetitions:
        detail1 = Competition.objects.get(event_name = detail.event)
        identify= detail.members.first().name if detail1.max_members==1 else detail.team_name
        print(identify)
        competition_details = {
            'event_name': detail1.event_name,
            'event_desc': detail1.event_desc,
            'solo_or_group':detail1.solo_or_group,
            'url':detail1.image.url,
            'identify':identify,
            'prize_worth':detail1.prize_worth,
        }

        competition_details_list.append(competition_details)
  print(competition_details_list)
  return render(request, 'eventRegistered/allEventsRegistered.html',  
                {'competition_details_list': competition_details_list,'registered_competitions_count':allcompetitions.count()})
    


@login_required(login_url='login')
def viewrules(request, slug):
    comp = Competition.objects.get(id=slug)
    return render(request, 'competitions/rules.html', {'comp': comp, 'active_page': 'rulebook'})

@login_required(login_url='login')
def memberedit(request, member_id):
    team = Team.objects.get(leader=request.user)
    member = TeamMembers.objects.get(id=member_id)
    print(member.phone)
    if request.method == 'POST':
        form = AddMemberForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            messages.success(request, 'Member details have been updated successfully')
            return redirect('TeamMembers')

    else:
        form = AddMemberForm(instance=member)

    return render(request, 'competitions/edit_member.html', {'form': form, 'active_page': 'competitions', 'referer': request.META.get('HTTP_REFERER')})

@login_required(login_url='login')
def delete_member(request,member_id):
    team = Team.objects.get(leader=request.user)
    member = TeamMembers.objects.get(id=member_id).delete()

    return redirect('TeamMembers')

@login_required(login_url='login')
def registercompetition(request, slug):
    comp = Competition.objects.get(id=slug)
    competition=Competition.objects.get(event_name=comp)
    if comp.portalUrl != '':
        return redirect(comp.portalUrl)
    reg_teams = CompTeam.objects.filter(leader=request.user, event=comp)
    team = Team.objects.get(leader=request.user)
    members=team.members.all()
    members_reg = []
    for rteam in reg_teams.all():
        members_reg += [member.id for member in rteam.members.all()]

    members_reg = set(members_reg)
    team_members = team.members.exclude(id__in=members_reg)
    if (len(team_members) < comp.min_members or len(team_members) == 0):
        messages.info(request, "Add " + str(comp.min_members-len(team_members)
                                            ) + " more members to register for " + comp.event_name)
        # return redirect('registercomp', pk=slug)
    if request.method == 'POST':
        ######################### saving team ####################################
        members_data = request.POST.get('members')
        members_uuids =  json.loads(f'[{" , ".join([f'"{uuid}"' for uuid in members_data.split(",")])}]')
        print ('these are the uuids of members ',members_uuids)
        number_of_members = len(members_uuids)
        if number_of_members < competition.min_members or number_of_members > competition.max_members:
            messages.error(request,f'The number of team members must be between {competition.min_members} and {competition.max_members} for this competition. Please select valid number of team members ')
            return redirect('registercomp',slug = slug)

        compteams= CompTeam.objects.create(
        event=comp, leader=request.user)
        if request.POST.get('team_name'):
            compteams.team_name=request.POST.get('team_name')
            compteams.save()
        # if not created:
        #     compteams.members.clear()
        team_members = []
        
        
        added_member_ids = set()
        for member in members_uuids:
            member_id = member

            if member_id not in added_member_ids:
                team_member = TeamMembers.objects.get(id=member_id)
                team_members.append(team_member)
                compteams.members.add(team_member)
                
                compteams.save()  
                added_member_ids.add(member_id)

        ######################### saving previpus performance form ####################################
        if comp.showPeformanceLink:
            prev= SubmitPerformance.objects.create(event=comp, team=compteams)
            prev.link = request.POST.get('link')
            prev.description = request.POST.get('description')
            prev.save()
            print('hello this is the list',team_members)
        ######################### mail system ####################################
        Leader=request.user
        subject = "Alcheringa Registration Confirmed: Get Ready for an Unforgettable Experience!"
        email_template_name = "competitions/registration_email.txt"
        c = {
            "name": Leader.fullname,
            "event": comp.event_name
        }
        user_email=Leader.email
        print(comp.event_name)
        email = render_to_string(email_template_name, c)
        try:
            send_mail(subject, email, settings.EMAIL_HOST_USER, [
                user_email], fail_silently=False)
            print("done")
        except BadHeaderError:
            return HttpResponse('Invalid header found.')
        for user in team_members:
            subject = "Alcheringa Registration Confirmed: Get Ready for an Unforgettable Experience!"
            email_template_name = "competitions/registration_email.txt"
            c = {
                "name": user.name,
                "event": comp.event_name
            }
            user_email=user.email
            print(comp.event_name)
            email = render_to_string(email_template_name, c)
            try:
                send_mail(subject, email, settings.EMAIL_HOST_USER, [
                    user_email], fail_silently=False)
                print("done")
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
        ##################################################################

        messages.success(
            request, 'You have registered your team for this event successfully')
        return redirect('RegisteredEvents')
    
    
    return render(request, 'competitions/comp.html', {
        'comp': comp,
        'team_members': team_members,
        'competition': competition,
        'team': team,
        'members_reg': members_reg,
        'members':members,
        'slug':slug
    })


@login_required(login_url='login')
def CancelRegistration(request, slug):
    team = CompTeam.objects.get(id=slug)
    print(team.event.pk, team, request.user,
          request.user.events_registered.all())
    team.delete()
    if not CompTeam.objects.filter(leader=request.user, event=team.event).first():
        comp = team.event
        print(comp)
        request.user.events_registered.remove(comp)
    return redirect('RegisteredEvents')


@login_required(login_url='login')
def UpdateRegistration(request, slug):
    reg_teams = CompTeam.objects.get(id=slug)
    comp = reg_teams.event
    team = Team.objects.get(leader=request.user)
    members_reg = []
    other_teams = CompTeam.objects.filter(leader=request.user, event=comp)
    for rteam in other_teams:
        members_reg += [member.id for member in rteam.members.all()]
    members_reg += [member.id for member in reg_teams.members.all()]
    members_reg = set(members_reg)
    team_members = team.members.exclude(id__in=members_reg)
    members_reg = reg_teams.members.all()
    # data = SubmitPerformance.objects.filter(team=reg_teams).first()
    if request.method == 'POST':
        ######################### saving team ####################################
        reg_teams.delete()
        compteams = CompTeam.objects.create(
            event=comp, leader=request.user)
        team_members = []
        for member in json.loads(request.POST.get('members')):
            print(str(member['id']))
            compteams.members.add(
                TeamMembers.objects.get(id=str(member['id'])))
            compteams.save()
        ######################### saving previpus performance form ####################################
        if comp.showPeformanceLink:
            prev = SubmitPerformance.objects.create(event=comp, team=compteams, link=request.POST.get(
                'link'), description=request.POST.get('description'))
            # if data != prev:
            prev.save()
        messages.success(
            request, 'You have registered your team for this event successfully')
        return HttpResponse("OK")
    return render(request, 'eventRegistered/compupdate.html', {'comp': comp, 'team_members': team_members, 'data': data, 'team_participant': members_reg, 'active_page': 'competitions'})


@login_required(login_url='login')
def add_member(request, slug=None):
    formset = AddMemberFormSet(request.POST or None)
    print(formset.is_valid())
    print(formset.errors)

    team = Team.objects.get(leader=request.user)
    members=team.members.all()
    print(team)
    if request.method == 'POST':
        print(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                gender = form.cleaned_data.get('gender')
                phone = form.cleaned_data.get('phone_number')

                if not name or not email or not gender or not phone:
                    messages.warning(request, 'All fields must be filled out')
                    return render(request, 'competitions/add_member.html', {'formset': formset})

                memberid = create_new_ref_number()  # Assumes you have a function to create a unique member ID
                new_member = TeamMembers.objects.create(
                    memberid=memberid,
                    name=name,
                    email=email,
                    gender=gender,
                    phone=phone
                )
                team.members.add(new_member)
                team.save()

            messages.success(request, 'You have successfully added new members to your team!')
            if slug:
                return redirect('registercomp', slug=slug)
            return redirect('add_member')

    return render(
        request,
        'eventRegistered/TeamMembers.html',
        {
            'formset' : formset,  # Correctly pass the formset to the template
            'active_page' : 'competitions',
            'referer' : request.META.get('HTTP_REFERER'),
            'slug' : slug,
            'members': members
        }
    )




@login_required(login_url='login')
def allEventsRegistered(request):
    user = request.user
   
    module_comp = user.events_registered.all()
    print(module_comp[0].image)
    # for module in module_comp:
    #     my_list = list()
    #     teams = CompTeam.objects.filter(leader = user, event = module)
    #     print('these are the following teams',teams)
    #     for team in teams:
    #         item = [team.members.all(),team.id]
    #         my_list.append(item)
    #     module.list =  my_list
    return render(request, 'eventRegistered/allEventsRegistered.html', { 'allcomp': module_comp, 'active_page':'registrations'})


@login_required(login_url='login')
def teamMembers(request,slug=None):
    formset = AddMemberFormSet(request.POST or None)
    print(formset.is_valid())
    print(formset.errors)

    team = Team.objects.get(leader=request.user)
    members=team.members.all()
    print(team)
    if request.method == 'POST':
        print(request.POST)
        if formset.is_valid():
            for form in formset:
                name = form.cleaned_data.get('name')
                email = form.cleaned_data.get('email')
                gender = form.cleaned_data.get('gender')
                phone = form.cleaned_data.get('phone_number')

                if not name or not email or not gender or not phone:
                    messages.warning(request, 'All fields must be filled out')
                    return render(request, 'competitions/add_member.html', {'formset': formset})

                memberid = create_new_ref_number()  # Assumes you have a function to create a unique member ID
                new_member = TeamMembers.objects.create(
                    memberid=memberid,
                    name=name,
                    email=email,
                    gender=gender,
                    phone=phone
                )
                team.members.add(new_member)
                team.save()

            messages.success(request, 'You have successfully added new members to your team!')
            if slug:
                return redirect('TeamMembers', slug=slug)
            return redirect('TeamMembers')

    return render(
        request,
        'eventRegistered/TeamMembers.html',
        {
            'formset' : formset,  # Correctly pass the formset to the template
            'active_page' : 'competitions',
            'referer' : request.META.get('HTTP_REFERER'),
            'slug' : slug,
            'members': members
        }
    )

def data(request, slug=None):
 if request.user.is_staff:
    if slug=='all':
        competitions1 = Competition.objects.all().filter(showPeformanceLink=True)
        competitions2 = Competition.objects.all().filter(showPeformanceLink = False)
        sub = SubmitPerformance.objects.all().filter(event__in=competitions1)
        compteam = CompTeam.objects.all().filter(event__in = competitions2)
        all_users = list(chain(sub,compteam))
        context = {
            'users':all_users,
        }
        return render(request,'data/all_users.html',context)    
    elif slug:
        comp=Competition.objects.get(id=slug)
        if comp.showPeformanceLink:
            all_users = SubmitPerformance.objects.all().filter(event=comp)
            # for comp in competitions:
            context = {
                'users':all_users,
            }
            return render(request,'data/all_users.html',context)
        else:
            all_users = CompTeam.objects.all().filter(event=comp)
            context = {
                'users':all_users,
            }
            return render(request,'data/all_users.html',context)
    # competitions1 = Competition.objects.all().filter(showPeformanceLink=True)
    # competitions2 = Competition.objects.all().filter(showPeformanceLink = False)
    # sub = SubmitPerformance.objects.all().filter(event__in=competitions1)
    # compteam = CompTeam.objects.all().filter(event__in = competitions2)
    # all_users = list(chain(sub,compteam))
    # # for comp in competitions:
    # context = {
    #     'users':all_users,
    # }
    competitions = Competition.objects.all()
    context={'comps':competitions}
    return render(request,'data/allcomp.html',context)
 return redirect('home')

def all_leaders(request):
    if request.user.is_staff:
        users=NewUser.objects.all().order_by("date_joined")
        context={
            "users":users
        }
        return render(request,'data/all_leaders.html',context)
    return redirect('home')

def home(request):
    competitions = Competition.objects.all()
    modules=Module.objects.all()
    return render(request, 'home/index.html', {'competitions': competitions,'modules':modules})