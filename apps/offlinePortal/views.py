from django.conf import settings
from django.shortcuts import render,redirect
from users.models import TeamMembers,Team
from competitions.models import Competition,SubmitPerformance,CompTeam
from users.models import NewUser, Price
from django.contrib import messages
from django.contrib.auth.decorators import login_required,permission_required
from django.utils.html import strip_tags
from django.utils.crypto import get_random_string
from itertools import chain
from datetime import date
import uuid
from django.core.mail import EmailMessage 
from django.http import HttpResponse
import io
from django.shortcuts import render
from datetime import date
import pdfkit
from django.template.loader import get_template
# from weasyprint import HTML
import csv

# Create your views here.
@login_required(login_url='login')
@permission_required('is_staff')
def home(request):
    return render(request,'offlinePortal/home.html',{'active_page':'registration'})

    
@login_required(login_url='login')
@permission_required('is_staff')
def search(request):
        if request.method == "POST":
            id =request.POST['alcherID']
            csrf=(request.POST['csrfmiddlewaretoken'])
            print(id)
            if(id!=''):
                if(id[0]=='A' and NewUser.objects.filter(alcherid=id).first()):
                    leader=NewUser.objects.filter(alcherid=id).first()
                    team = Team.objects.get(leader=leader)
                    context = {
                        'leader':leader,
                        'team':team,
                        'active_page':'universal_search'
                    }
                    return render(request,'offlinePortal/universalSearch.html',context)
                elif(id[0]=='M' and TeamMembers.objects.filter(memberid=id).first()):
                    member=TeamMembers.objects.filter(memberid=id).first()
                    team = Team.objects.get(members=member)
                    context = {
                        'member':member,
                        'team':team,
                        'id':id,
                        'csrf':csrf,
                        'active_page':'universal_search'
                    }
                    return render(request,'offlinePortal/universalSearch.html',context)
                else:
                    messages.error(request,'Please enter a correct ID')
                    return render(request,'offlinePortal/universalSearch.html',{'active_page':'universal_search'})
            else:
                messages.error(request,'Enter ID .')
                return render(request,'offlinePortal/universalSearch.html',{'active_page':'universal_search'})


        return render(request,'offlinePortal/universalSearch.html',{'active_page':'universal_search'})

@login_required(login_url='login')
@permission_required('is_staff')
def eventwise_search(request):

    comps = Competition.objects.all()
    if request.method == "POST":
        selection = request.POST['competition']
        competition= Competition.objects.filter(id=selection).first()
        competitions1 = Competition.objects.all().filter(showPeformanceLink=True)
        competitions2 = Competition.objects.all().filter(showPeformanceLink = False)
        if (competition in competitions1):
            submissions=SubmitPerformance.objects.all().filter(event=competition).select_related("team").prefetch_related("team__members")
            if(submissions.count()):
                context={
                    "competition":competition,
                    "submissions":submissions,
                    'comps':comps,
                }
                return render(request,'offlinePortal/eventwise_search.html',context)
            else:
                context={
                    'message':'No registration for ',
                    'comps':comps,
                    'competition':competition
                }
                return render(request,'offlinePortal/eventwise_search.html',context)

        elif (competition in competitions2):
            competitions_without_submissions = CompTeam.objects.all().filter(event=competition)
            if(competitions_without_submissions.count()):
                context={
                    "competition":competition,
                    "comp_wo_sub":competitions_without_submissions,
                    'comps':comps,
                }
                return render(request,'offlinePortal/eventwise_search.html',context)
            else:
                context={
                    'message':'No registration for ',
                    'comps':comps,
                    'competition':competition
                }
                return render(request,'offlinePortal/eventwise_search.html',context)
        else:
            context={
                'message':'No registration for ',
                'comps':comps,
                'competition':competition
            }
            return render(request,'offlinePortal/eventwise_search.html',context)
    return render(request,'offlinePortal/eventwise_search.html',{'comps':comps,'active_page':'eventwise_search'})

@login_required(login_url='login')
@permission_required('is_staff')
def eventRegister(request):
    if request.method=="POST":
        members=request.POST.getlist('member')
        competition=Competition.objects.filter(id=request.POST.get('competition')).first()
        id=request.POST.get('team')
        leader=NewUser.objects.filter(alcherid=id).first();
        # team=Team.objects.filter(leader=leader).first()
        team1=CompTeam.objects.filter(leader=leader).first()
        event=CompTeam(event=competition,leader=leader)
        event.save()
        if competition.showPeformanceLink:
            prev = SubmitPerformance.objects.create(event=competition, team=team1, link=request.POST.get(
                'link'),description=request.POST.get('description'))
            prev.save()
        for member in members:
            event.members.add(TeamMembers.objects.filter(memberid=member).first())
    return render(request,"offlinePortal/eventRegister.html",{"active_page":"event_registration"})


@login_required(login_url='login')
@permission_required('is_staff')
def searchTeam(request):
    if request.method=="POST":
        id=request.POST.get('alcherid')
        leader=NewUser.objects.filter(alcherid=id).first()
        if leader==None:
            messages.error(request,'Team Not Found')
            return render(request,"offlinePortal/eventRegister.html",{'active_page':'event_registration'})
        print(id,leader)
        team = Team.objects.get(leader=leader)
        competitions=Competition.objects.all()
        members=team.members.all()
        print(members)
    return render(request,"offlinePortal/eventRegister.html",{"team":team,"members":members,"competitions":competitions,"id":id,'active_page':'event_registration'})

def genINV():
    inv='INV-'+get_random_string(length=12)
    return inv


@login_required(login_url='login')
@permission_required('is_staff')
def roomAllotment(request):
        if request.method == "POST":
            if(request.POST['accomodation'] != '0'):
                # print(request.POST)
                team =  Team.objects.get(id = request.POST['teamId'])
                csrf=(request.POST['csrfmiddlewaretoken'])
                type1count=0
                type2count=0
                type3count=0
                type1days=0
                type2days=0
                type3days=0
                team.save()
                
                for member in team.members.all():
                    if( request.POST[member.memberid + "acc"]!= '0'):
                        member.accomodation = True
                        member.daysStay = request.POST[member.memberid + "stay"]
                        
                        member.accomodation_type=request.POST[member.memberid+"acctype"]
                        
                        member.save()
                        if(member.accomodation_type=='type1'):
                            type1count+=1
                            type1days+=int(member.daysStay)
                        elif(member.accomodation_type=='type2'):
                            type2count+=1
                            type2days+=int(member.daysStay)
                        elif(member.accomodation_type=='type3'):
                            type3count+=1
                            type3days+=int(member.daysStay)
                
                context ={
                    "blankets":request.POST['blankets'],
                  
                    "total": request.POST['total'],
                    "team": team,
                   
                    "accomodation":int(request.POST['AccomodationPrice']),
                    'active_page':'accomodation',
                    'alcherid':team.leader.alcherid,
                    "invno":genINV(),
                    "invdate":date.today(),
                    "leadername":team.leader.fullname,
                    "collegename":team.leader.collegename,
                    "phoneno":team.leader.phone_number,
                    "accomodation_type":request.POST[member.memberid+"acctype"],
                    "type1count":type1count,
                    "type2count":type2count,
                    "type3count":type3count,
                    "type1days":type1days,
                    "type2days":type2days,
                    "type3days":type3days

                }
                
                
              
                team.blankets+= int(request.POST['blankets'])
                team.totalPaid+=int(request.POST['AccomodationPrice'])
                
                # Price.price = team.totalPaid 
                
                team.save()
                
                template= get_template('offlinePortal/receipt.html')
                html_content= template.render(context)
                
                # pdf = HTML(string=html_content, base_url=request.build_absolute_uri()).write_pdf()
                 
                # response = HttpResponse(pdf, content_type='application/pdf')
                # response['Content-Disposition'] = 'attachment; filename="invoice.pdf"'
                # return response
                # return render(request,'offlinePortal/receipt.html',context)
                
                leader_email= team.leader.email
                email=EmailMessage(   
                    subject="Alcheringa Stay Invoice",
                    body="Here is your invoice",
                    to=[leader_email]
                )

                
                email.attach('invoice.pdf', pdf, 'application/pdf')
                email.send()
                
                messages.success(request, 'Mail sent to ' + leader_email)
                
                return render(request,'offlinePortal/receipt.html', context)
                # return render(request,'offlinePortal/receipt.html',context)
            
            id =request.POST['alcherID']
            csrf=(request.POST['csrfmiddlewaretoken'])
            if(id!=''):
                if(id[0]=='A' and NewUser.objects.filter(alcherid=id).first()):
                    leader=NewUser.objects.filter(alcherid=id).first()
                    team = Team.objects.get(leader=leader)
                    context = {
                        'leader':leader,
                        'team':team,
                        'team_members': team.members.all(),
                        'active_page':'accomodation'
                    }
                    return render(request,'offlinePortal/roomAllot.html',context)
                elif(id[0]=='M' and TeamMembers.objects.filter(memberid=id).first()):
                    member=TeamMembers.objects.filter(memberid=id).first()
                    team = Team.objects.get(members=member)
                    context = {
                        'member':member,
                        'team':team,
                        'id':id,
                        'team_members': team.members.all(),
                        'active_page':'accomodation',
                        'csrf':csrf,
                    }
                    return render(request,'offlinePortal/roomAllot.html',context)
                elif NewUser.objects.filter(email=id).exists():
                    print(id)
                    leader=NewUser.objects.get(email=id)
                    team = Team.objects.get(leader=leader)
                    context = {
                        'leader':leader,
                        'team':team,
                        'team_members': team.members.all(),
                        'active_page':'accomodation'
                    } 
                    return render(request,'offlinePortal/roomAllot.html',context)
                else:
                    messages.error(request,'Please enter a correct ID')
                    return render(request,'offlinePortal/roomAllot.html',{'active_page':'accomodation'})
            else:
                messages.error(request,'Enter ID .')
                return render(request,'offlinePortal/RoomAllot.html',{'active_page':'accomodation'})
            
        # with open(input_filename) as f:
         #     pdf= pdfkit.from_file(f, 'out.pdf')
    


        return render(request,'offlinePortal/roomAllot.html',{'active_page':'accomodation'})

@login_required(login_url='login')
@permission_required('is_staff')
def blankets_dues(request):
    teams=Team.objects.all()
    context={'teams':teams,'active_page':'blankets_dues'}
    return render(request,'offlinePortal/blankets_dues.html',context)

@login_required(login_url='login')
@permission_required('is_staff')
def edit_blankets_dues(request):
    id=request.GET.get('team')
    print(request.POST)
    if request.method=='POST':
        teamid = request.POST['teamid']
        print(request.POST)
        team = Team.objects.get(id=teamid)
        blankets1=request.POST['blanketUpdate']
     
        team.blankets=blankets1
       
        team.save()
        context={'team':team,'active_page':'edit_blankets_dues'}
        return render(request,'offlinePortal/edit_blanketdues.html',context)
    if id:
        context={'team':'','active_page':''}
        if id[0] =='A':
            user = NewUser.objects.filter(alcherid = id).first()
            team = Team.objects.get(leader = user)
            context={'team':team,'active_page':'edit_blankets_dues'}
            print(context,user)

        if id[0] =='M':
            member = TeamMembers.objects.filter(memberid = id)
            teams = Team.objects.get(members__in = member)
            context={'team':teams,'active_page':'edit_blankets_dues'}
        return render(request,'offlinePortal/edit_blanketdues.html',context)
    return render(request,'offlinePortal/edit_blanketdues.html',{'active_page':'edit_blankets_dues'})


# def home(request):
#     if request.POST:
#         print(request.POST.get('name'))
#     return render(request,'offlinePortal/register.html')

def create_new_ref_number():
    memberid = "MEM-"
    memberid += str(TeamMembers.objects.count()+5001)+"-"
    memberid += get_random_string(length=4)
    if TeamMembers.objects.filter(memberid=memberid).exists():
        return create_new_ref_number()
    return memberid

def create_new_ref_Number():
    leader_id = "ALC-"
    leader_id += str(Team.objects.count()+5001)+"-"
    leader_id += get_random_string(length=4)
    if NewUser.objects.filter(alcherid=leader_id).exists():
        return create_new_ref_number();
    if Team.objects.filter(leader_id=leader_id).exists():
        return create_new_ref_Number()
    return leader_id


@login_required(login_url='login')
@permission_required('is_staff')
def updateData(request):
    if request.method=='POST':
        try:
            alcher_id=create_new_ref_Number()
            teamLeader=NewUser(fullname=request.POST.get('teamLeaderName'),city=request.POST.get('city'),phone=request.POST.get('teamLeaderContact'),
            collegename=request.POST.get('college'), email=request.POST.get('teamLeaderEmail'),gender=request.POST.get('teamLeaderGender'),username=get_random_string(length=32),alcherid=alcher_id).save()
            print(teamLeader)
            
        except Exception as e:
            print(e)
     

        try:
             
             member_names = request.POST.getlist('name')
             member_emails=request.POST.getlist('email')
             member_contactNos=request.POST.getlist('phone')
             member_genders=request.POST.getlist('gender')
            #  print(member_names,member_contactNos,member_genders,member_emails)
             members = [TeamMembers(name=member_names[i], email=member_emails[i],phone=member_contactNos[i], gender=member_genders[i],memberid=create_new_ref_number()) for i in range(len(member_names))]
            #  print(members) 
             TeamMembers.objects.bulk_create(members)
         
             users = NewUser.objects.filter( phone=request.POST.get('teamLeaderContact'))
             if users.exists():
                 leader = users.first()
      
             else:
                 print("No matching NewUser object was found")             
             team = Team.objects.filter(leader=leader).first()
             team.Accomodation=request.POST.get(' Accomodation')
             team.name=request.POST.get('teamName')
             team.save()
             for i in range(len(member_emails)): 
                 try:
                     member = TeamMembers.objects.get(email=member_emails[i])
                     print(member_emails)
                 except TeamMembers.DoesNotExist:
                     print(f"No matching TeamMembers object was found for email {member_emails[i]}")
                     continue
                 team.members.add(member)
                 team.save()
             print(leader)
              
             
        except Exception as e:
            print(e)

        leader_memeber = TeamMembers.objects.filter(email = request.POST.get('teamLeaderEmail')).first()
        print(leader_memeber)
        leader_memeber.name = request.POST['teamLeaderName']
        leader_memeber.gender = request.POST['teamLeaderGender']
        leader_memeber.save()
        print(alcher_id)
        messages.info(request,f'Your AlcherID is {alcher_id}.')
        return redirect('/offlineportal')

@login_required(login_url='login')
@permission_required('is_staff')
def saveEditData(request):
    
 if request.method=='POST':
        alcherid=request.POST.get('hidden_field')
        print(alcherid)
        
        clgname=request.POST.get('college')
        city=request.POST.get('city')
        
        name=request.POST.get('teamName')
        newuser=NewUser.objects.filter(alcherid=alcherid).first()
        
        print(newuser.email)
        team = Team.objects.filter(leader=newuser).first()
        print(team)
        print(alcherid)
        # print(clgname)
        # newuser(clgname).save()
        newuser.collegename=clgname
        newuser.city=city
        team.name=name
       
        print(newuser)
        try:  
           newuser.save()
        except Exception as e:
            print(e)
        memdtls=[]
    # print(memdt)
    
        

        
        member=Team.objects.get(leader=newuser).members.all()
            # print(teamLeader)
            
        for mem in member:
            memdtls.append(TeamMembers.objects.get(email=mem))
        for member in memdtls:
            idname=member.id+"-name"
            name=request.POST.get(idname)
            
            member.name=name
            email=request.POST.get(member.id+"-email")
            member.email=email
            phone=request.POST.get(member.id+"-phone")
            member.phone=phone
            gender=request.POST.get(member.id+"-gender")
            member.gender=gender
    
            member.save()

        member_names = request.POST.getlist('name')
        member_emails=request.POST.getlist('email')
        member_contactNos=request.POST.getlist('phone')
        member_genders=request.POST.getlist('gender')
    #  print(member_names,member_contactNos,member_genders,member_emails)



        members = [TeamMembers(name=member_names[i], email=member_emails[i],phone=member_contactNos[i], gender=member_genders[i],memberid=create_new_ref_number()) for i in range(len(member_names))]
    #  print(members) 
        TeamMembers.objects.bulk_create(members)       
        users = NewUser.objects.filter( phone=request.POST.get('teamLeaderContact'))
        if users.exists():
            leader = users.first()

        else:
            print("No matching NewUser object was found")             
       
        for i in range(len(member_emails)): 
            try:
                member = TeamMembers.objects.get(email=member_emails[i])
                print(member_emails)
            except TeamMembers.DoesNotExist:
                print(f"No matching TeamMembers object was found for email {member_emails[i]}")
                continue
            team.members.add(member)
            team.save()      

           
   
        return render(request,'offlinePortal/edit.html')
@login_required(login_url='login')
@permission_required('is_staff')
def editData(request):
    query=request.GET.get('edit_id')
    teamLeader=NewUser.objects.filter(alcherid=query).first()
    # mems=Team.members.get_forward_related_filter(leader=teamLeader)
    # print(teamLeader)
    # print(member)
    memdtls=[]
    # print(memdt)
    print(teamLeader)
    if teamLeader:
        member=Team.objects.get(leader=teamLeader).members.all()
        # print(teamLeader)
        print(member)
        team=Team.objects.get(leader=teamLeader)
        for mem in member:
            memdtls.append(TeamMembers.objects.get(email=mem))
            print(memdtls)
        params={'team':teamLeader,'memdtls':memdtls,'mem':team}
        # print(team.Accomodation)
        # for member in Teammembers.members:
        #     print(member)
        return render(request,'offlinePortal/saveEdit.html',params)
    return render(request,'offlinePortal/edit.html')


@login_required(login_url='login')
@permission_required('is_staff')
def deleteUser(request,memid):
    # memid=request.POST.get('hidden_field2')
    print(memid)
    memb=TeamMembers.objects.filter(memberid=memid).first()
    memb.delete()
    # alcid=request.GET.get('edit_id')
    
    return render(request,'offlinePortal/deleteconfirm.html')


@login_required(login_url='login')
@permission_required('is_staff')
def saveEdit(request):
     return render(request,'offlinePortal/saveEdit.html')
 
 
 
@login_required(login_url='login')
@permission_required('is_staff')
def general_search(request):
     return render(request,'offlinePortal/general_search.html')
 
 

@login_required(login_url='login')
@permission_required('is_staff')
def all_users(request):
    if request.user.is_staff:
        users=NewUser.objects.all().order_by("date_joined")
        competitions1 = Competition.objects.all().filter(showPeformanceLink=True)
        competitions2 = Competition.objects.all().filter(showPeformanceLink = False)
        sub = SubmitPerformance.objects.all().filter(event__in=competitions1)
        compteam = CompTeam.objects.all().filter(event__in = competitions2)
        all_users = list(chain(sub,compteam))
        # for comp in competitions:
        context = {
            'users':all_users,
        }
        return render(request,'offlinePortal/all_users.html',context)
    return redirect('login')

@login_required(login_url='login')
@permission_required('is_staff')
def all_leaders(request):
    if request.user.is_staff:

        users=NewUser.objects.all().order_by("date_joined")
        context={
            "users":users
        }
        return render(request,'offlinePortal/all_leaders.html',context)
    return redirect('login')

from django.views.decorators.csrf import csrf_exempt
@csrf_exempt
def pdupdate(request):
    if request.method=="POST":
        csv_file=request.FILES['document']
        file_data=csv_file.read().decode("ISO-8859-1")
        print(file_data)
        a=1
        csv_data=file_data.split('\n')
        for x in csv_data:
            fields=x.split(',')
            emailid=NewUser.objects.filter(email=fields[2])
            if emailid:
                print(emailid)
                emailid="same"+str(uuid.uuid4())+fields[2]
            else:
                emailid=fields[2]
            user=NewUser(alcherid=create_new_ref_Number(),fullname=fields[1],username="pd"+str(a),email=emailid,phone=fields[4],collegename=fields[3],about=fields[5])
            a+=1
            user.save()
            event=Competition.objects.filter().first()
            comp=CompTeam(event=event,leader=user)
            comp.save()
    return render(request,'offlinePortal/csv_upload.html')


# @csrf_exempt
# def vogueupdate(request):
#     if request.method=="POST":
#         csv_file=request.FILES['document']
#         file_data=csv_file.read().decode("ISO-8859-1")
#         print(file_data)
#         csv_data=file_data.split('\n')
#         for x in csv_data:
#             fields=x.split(',')
#             print(fields)
#             emailid=NewUser.objects.filter(email=fields[6])
#             if emailid:
#                 print(emailid)
#                 emailid="same"+str(uuid.uuid4())+fields[6]
#             else:
#                 emailid=fields[6]
#             user=NewUser(alcherid=create_new_ref_Number(),fullname=fields[2],username=("vogue"+str(uuid.uuid4)),email=emailid,phone=fields[6]);
#             user.save()
#             event=Competition.objects.filter(event_name=fields[5]).first()
#             comp=CompTeam(event=event,leader=user)
#             comp.save()
#             team=Team(name=fields[1],leader=user)
#             members=fields[3].split('|')
#             for member in members:
#                 mem=TeamMembers(memberid=create_new_ref_number(),email=(str(uuid.uuid4())+"@member.com"),name=member)
#                 mem.save()
#                 team.members.add(TeamMembers.objects.filter(memberid=mem.memberid).first())
#             team.save()
#     return render(request,'offlinePortal/csv_upload.html')




def your_view(request):
    current_date = date.today()
    return render(request, 'offlinePortal/roomAllot.html', {'current_date': current_date})


def generate_invoice(request):
    # leader=NewUser.objects.filter(alcherid=id).first()
    # team = Team.objects.get(leader=request.user)
    email=EmailMessage(
        subject="That's the subject",
        body="That's your message body",
        from_email= settings.EMAIL_HOST_USER,
        to=['sarveshsmurkute@gmail.com']
    )

    # email.attach_file(pdf)
    email.send()
    
    # messages.success('Message sent to ' + leader.email) 
    return render (request,  'offlinePortal/reciept.html' )

def htmltopdf(request):
    path_wkhtmltopdf = 'C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe'  # This may vary depending on your system
    config = pdfkit.configuration(wkhtmltopdf=path_wkhtmltopdf)
    
    # Use the configuration when generating PDF
    pdf= pdfkit.from_url('http://google.com', 'out.pdf', configuration=config)
    
    

@csrf_exempt
def vogueupdate(request):
    if request.method=="POST":
        csv_file=request.FILES['document']
        file_data=csv_file.read().decode("ISO-8859-1")
        
        csv_data=file_data.split('\n')
        y = 0
        for x in csv_data:
            if y==0:
                y=1
                continue
            fields=x.split(',')
            
            
            emailid=NewUser.objects.filter(email=fields[3])
            if emailid:
                print(emailid)
                emailid="same"+str(uuid.uuid4())+fields[3]
            else:
                emailid=fields[3]
            user=NewUser(alcherid=create_new_ref_Number(),fullname=fields[2],username=("vogue"+str(uuid.uuid4())),email=emailid,phone_number=fields[4])
            print(user.username)
            user.save()
            y+=1
            # event=Competition.objects.filter(event_name=fields[5]).first()
            # comp=CompTeam(event=event,leader=user)
            # comp.save()
            team=Team(name=fields[0],leader=user)
            team.save()
            member=fields[7]
            if member == '\r':
                continue
            else: 
                member=fields[7].split('~')
                # print(member)
                
                for z in member: 
                    
                    if z == '\r':
                        continue
                    else:
                        mem_data= z.split('|')
                        mem=TeamMembers(memberid=create_new_ref_number(),email=mem_data[1],name=mem_data[0], phone=mem_data[2])
                        mem.save()
                        team.members.add(mem)
                        team.save()
        print(y)
                        
                
                    
    return render(request,'offlinePortal/csv_upload.html')


@csrf_exempt
def rockoupdate(request):
    if request.method=="POST":
        csv_file=request.FILES['document']
        file_data=csv_file.read().decode("ISO-8859-1")
        
        csv_data=file_data.split('\n')
        y = 0
        for x in csv_data:
            if y==0:
                y=1
                continue
            fields=x.split(',')
            
            
            emailid=NewUser.objects.filter(email=fields[7])
            if emailid:
                print(emailid)
                emailid="same"+str(uuid.uuid4())+fields[7]
            else:
                emailid=fields[7]
            user=NewUser(alcherid=create_new_ref_Number(),fullname=fields[4],username=("vogue"+str(uuid.uuid4())),email=emailid,phone_number=fields[6])
            print(user.username)
            user.save()
            y+=1
            # event=Competition.objects.filter(event_name=fields[5]).first()
            # comp=CompTeam(event=event,leader=user)
            # comp.save()
            team=Team(name=fields[0],leader=user)
            team.save()
            member=fields[8]
            if member == '\r':
                continue
            else: 
                member=fields[8].split('~')
                # print(member)
                
                for z in member: 
                    
                    if z == '\r':
                        continue
                    else:
                        mem_data= z.split('|')
                        
                        mem=TeamMembers(memberid=create_new_ref_number(),email=mem_data[3],name=mem_data[0], phone=mem_data[2])
                        mem.save()
                        team.members.add(mem)
                        team.save()
        print(y)
                        
                
                    
    return render(request,'offlinePortal/csv_upload.html')