from django.contrib import admin
from django.urls import include, path
from . import views
app_name="helpdesk"
urlpatterns = [
    path('login',views.login_view , name='login_view'),
    path('logging_in',views.logging_in , name='logging_in'),
    path('list-tickets.html',views.list_tickets.as_view() , name='list-tickets'),
    path('new_ticket.html',views.new_ticket , name='new_ticket'),
    path('send_ticket',views.send_ticket , name='send_ticket'),
    path('faq.html',views.faq , name='faq'),
    path('view-ticket_<int:ticket_num>',views.view_ticket , name='view_ticket'),
    path('finish_ticket_<int:ticket_num>',views.finish_ticket , name='finish_ticket'),
    path('list-messages.html',views.list_messages , name='list_messages'),
    path('view_message_<int:message_num>',views.view_message , name='view_message'),
    path('new-message.html',views.new_message , name='new_message'),
    path('send_message',views.send_message , name='send_message'),
    path('list-tickets-admin.html',views.list_tickets_admin.as_view(), name='list_tickets_admin'),
    path('view-ticket_admin_<int:ticket_num>',views.view_ticket_admin , name='view_ticket_admin'),
    path('accept_ticket_<int:ticket_num>',views.accept_ticket , name='accept_ticket'),
    path('send_ticket_message',views.send_ticket_message,name='send_ticket_message'),
    path('logout',views.logout_view,name='logout')
]
