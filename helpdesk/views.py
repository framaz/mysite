from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.db.models import Q
from datetime import datetime
from . import models
# Create your views here.
def login_view(request):
    if request.user.is_authenticated:
        return redirect(reverse('helpdesk:list-tickets'))
    context={}
    try:
        if(request.GET['type']=='wrong_pass'):
            context['wrong_pass']=True
    except:
        pass
    return render(request,"helpdesk/index.html",context)
def logging_in(request):

    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect(reverse('helpdesk:list-tickets'))
    else:
        # Return an 'invalid login' error message.
        return redirect(reverse('helpdesk:login_view')+"?&type=wrong_pass")
        
class list_tickets(LoginRequiredMixin,generic.ListView):
    template_name = 'helpdesk/list-tickets.html'
    login_url = 'helpdesk:login_view'
    redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.first_name + " " + self.request.user.last_name
        if models.EmployeesInDepartments.objects.filter(person = self.request.user).count()>0:
            context['isWorker'] = True
        return context
    def get_queryset(self):
        result_list=models.Ticket.objects.filter(requestor=self.request.user)
        return result_list.filter(finished=False,deleted=False).order_by('id')
@login_required
def new_ticket(request):
    context = {"user":request.user.first_name+" "+request.user.last_name,
                "departments":models.Department.objects.all()}
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    return render(request,"helpdesk/new-ticket.html",context)
@login_required
def send_ticket(request):
    exp_date = request.POST['date']
    translated_date= exp_date[6:10] + "-" + exp_date[0:2] + "-" + exp_date[3:5]
    if datetime.strptime(translated_date, '%Y-%m-%d')<timezone.now().replace(tzinfo=None):
        return redirect('helpdesk:new_ticket')
    models.Ticket.objects.create(requestor = request.user,
                            theme = request.POST['theme'],
                            targeted_department = models.Department.objects.get(pk=request.POST['division']),
                            place = request.POST['room'],
                            exp_date = translated_date,
                            details = request.POST['message'],
                            pub_date = timezone.now()
                        )
    return redirect('helpdesk:list-tickets')
def get_user_num(lista,request):
    def name_checker(message,name):
        if(message.find(name)==0):
            return 0
        return 1
    return list(map(lambda item: (item,name_checker(item,request.user.first_name + " " + request.user.last_name)),lista))
@login_required
def view_ticket(request,ticket_num):
    context = {"obj": get_object_or_404(models.Ticket,pk=ticket_num,deleted=False,finished=False),
                "user": request.user.first_name + " " + request.user.last_name}
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    result_list=models.Ticket.objects.filter(requestor=request.user).order_by('-id')
    context["tickets"] = result_list.filter(finished=False,deleted=False)
    context["chat"]=get_user_num(context["obj"].chat.split("\n"),request)
    try:
        context["chat"].pop(0)
    except ValueError:
        context["chat"]=context["obj"].chat.split("\n")
    if context["obj"].requestor == request.user:
        return render(request,"helpdesk/view-ticket.html",context)
    else:
        return redirect(reverse('helpdesk:list-tickets'))
@login_required
def finish_ticket(request,ticket_num):
    obj=models.Ticket.objects.get(pk=ticket_num)
    if request.POST["result"] == 'Засчитать':
        obj.finished=True
    if request.POST["result"] == 'Удалить':
        print(request.POST["result"])
        obj.deleted=True
    obj.save()
    return redirect('helpdesk:list-tickets')
@login_required
def faq(request):
    context = {"questions":models.QuestionsAndAnswers.objects.all(),
                "user": request.user.first_name + " " + request.user.last_name}
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    return render(request,"helpdesk/faq.html",context)
@login_required
def list_messages(request):
    context = {"user": request.user.first_name + " " + request.user.last_name,
                }
    messages_array = models.Message.objects.filter(Q(sender = request.user) | Q(reciver = request.user)).order_by('-date')
    context["messages"] = messages_array
    context["watcher"] = request.user
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    return render(request,"helpdesk/list-messages.html",context)
@login_required
def view_message(request,message_num):
    message = get_object_or_404(models.Message,pk=message_num,deleted=False)
    if message.sender != request.user and message.reciver != request.user:
        return redirect('helpdesk:list_messages')
    context = {"user": request.user.first_name + " " + request.user.last_name,
                   "message": message,
                   "watcher": request.user}
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    return render(request,'helpdesk/view-message.html',context)
@login_required
def new_message(request):
    context = {"user": request.user.first_name + " " + request.user.last_name,
               "tickets": models.Ticket.objects.filter(Q(requestor = request.user)|Q(worker = request.user),deleted=False,finished=False,worker__isnull=False)}
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
            context['isWorker'] = True
    return render(request,'helpdesk/new-message.html',context)
@login_required
def send_message(request):
    cur_ticket = get_object_or_404(models.Ticket,pk=request.POST["theme"],deleted=False,finished=False,worker__isnull=False)
    if cur_ticket.worker == request.user:
        target = cur_ticket.requestor
    else:
        target = cur_ticket.worker
    models.Message.objects.create(sender = request.user,
                            reciver = target,
                            text = request.POST["message_to_get"],
                            ticket = cur_ticket,
                            date = timezone.now()
                        )
    return redirect('helpdesk:list_messages')
    
class list_tickets_admin(LoginRequiredMixin,generic.ListView):
    template_name = 'helpdesk/list-tickets.html'
    login_url = 'helpdesk:login_view'
    redirect_field_name = 'redirect_to'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['user'] = self.request.user.first_name + " " + self.request.user.last_name
        if models.EmployeesInDepartments.objects.filter(person = self.request.user).count()>0:
            context['isWorker'] = True
        context['isAdmining'] = True
        return context
    def get_queryset(self):
        departments_querySet = models.EmployeesInDepartments.objects.filter(person = self.request.user)
        department_list = []
        for department in departments_querySet.all():
            department_list.append(department.department.pk)

        result_list=models.Ticket.objects.filter(targeted_department__pk__in=department_list,finished=False,deleted=False)
        return result_list.order_by('-pub_date')
@login_required
def send_ticket_message(request):
    ticket=models.Ticket.objects.get(pk=request.POST["ticket_num"])
    message=request.POST["chat-message"].replace("\n"," ")
    ticket.chat+="\n"+request.user.first_name+" "+request.user.last_name+":"+message
    ticket.save()
    if request.POST["user_type"] == "user":
        return redirect('helpdesk:view_ticket',ticket_num=ticket.pk)
    else:
        return redirect('helpdesk:view_ticket_admin',ticket_num=ticket.pk)
    
@login_required
def view_ticket_admin(request,ticket_num):
    context = {"obj": get_object_or_404(models.Ticket,pk=ticket_num,deleted=False,finished=False),
                "user": request.user.first_name + " " + request.user.last_name}
    get_object_or_404(models.EmployeesInDepartments,person=request.user,department=context["obj"].targeted_department)
    departments_querySet = models.EmployeesInDepartments.objects.filter(person = request.user)
    context["chat"]=get_user_num(context["obj"].chat.split("\n"),request)
    try:
        context["chat"].pop(0)
    except ValueError:
        context["chat"]=context["obj"].chat.split("\n")
    department_list = []
    for department in departments_querySet.all():
        department_list.append(department.department.pk)
    result_list=models.Ticket.objects.filter(targeted_department__pk__in=department_list,finished=False,deleted=False)
    result_list.order_by('-pub_date')
    context["tickets"]=result_list
    if models.EmployeesInDepartments.objects.filter(person = request.user).count()>0:
        context['isWorker'] = True
    return render(request,'helpdesk/view-ticket_admin.html',context)
@login_required
def accept_ticket(request,ticket_num):
    ticket = get_object_or_404(models.Ticket,pk=ticket_num,deleted=False,finished=False,worker=None)
    if models.EmployeesInDepartments.objects.filter(person = request.user,department = ticket.targeted_department).count()>0:
        ticket.worker=request.user
        ticket.save()
    return redirect('helpdesk:list_tickets_admin')
def logout_view(request):
    logout(request)
    return redirect('helpdesk:login_view')
    