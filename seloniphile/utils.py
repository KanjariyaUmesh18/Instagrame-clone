from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db.models import Q
from .models import *


def get_or_create_chatRoom(user1,user2):

    conversation = ChatRoom.objects.filter(Q(user1 = user1,user2 = user2) | Q(user1 = user2 , user2 = user1 )).first()
    
    if conversation:
        return conversation
    
    ChatRoom.objects.create(user1 = user1,user2 = user2)