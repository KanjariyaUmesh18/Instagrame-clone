from enum import unique
from django.db import models
import math,datetime
from django.utils import timezone

# Create your models here.
class InstaUser(models.Model):
    GENDER_CHOICES = (
        ('male','Male'),
        ('female','Female'),
    )
    username = models.CharField(max_length=100,unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    profile_pic = models.FileField(upload_to='profile_pics/', blank=True, null=True)
    gender = models.CharField(max_length=10,choices=GENDER_CHOICES,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

class instapost(models.Model):
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    image = models.FileField(upload_to='posts/')
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    tagged_users = models.ManyToManyField(InstaUser, blank=True,related_name="tagged_users")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
    
    def whenpublished(self):

        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            
            else:
                return str(years) + " years ago"

class FollowUserd(models.Model):
    following = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="following")
    following_person = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="following_person")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.following.name} - following {self.following_person.name}"
    
class Notification(models.Model):
    NOTIFICATION_TYPE = (
        ('follow','Follow'),
        ('like','Like'),
        ('comment','Comment')
    )
    sender = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="sender_notification")
    reciever = models.ForeignKey(InstaUser, on_delete=models.CASCADE,related_name="reciever_notification")
    notification_type = models.CharField(max_length=50,choices=NOTIFICATION_TYPE)
    message = models.CharField(max_length=50,null=True,blank=True)
    post_fk = models.ForeignKey(instapost, on_delete=models.CASCADE,null=True,blank=True)
    read_status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def whenpublished(self):

        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            
            else:
                return str(years) + " years ago"
            
    def __str__(self):
        return f"{self.sender.username} {self.message} {self.reciever.username}"

class LikeUnlike(models.Model):
    user_fk = models.ForeignKey(InstaUser,on_delete=models.CASCADE,related_name="liked_by")
    post_fk = models.ForeignKey(instapost,on_delete=models.CASCADE,related_name="like_post")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_fk','post_fk']

    def __str__(self):
        return f"{self.user_fk.username} liked  {self.post_fk.caption }"
    
class Comment(models.Model):
    user_fk = models.ForeignKey(InstaUser,on_delete=models.CASCADE)
    post_fk = models.ForeignKey(instapost,on_delete=models.CASCADE)
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment
    
class CreateReel(models.Model):
    user = models.ForeignKey(InstaUser, on_delete=models.CASCADE)
    video = models.FileField(upload_to='reels/')
    caption = models.TextField(blank=True, null=True)
    location = models.CharField(max_length=100, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.caption
    
class CreateStory(models.Model):
    user = models.ForeignKey(InstaUser,on_delete=models.CASCADE)
    story_image = models.FileField(upload_to="Story_image/")
    story_caption = models.TextField(max_length=200,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(hours=24)

    def __str__(self):
        return f"{self.user.username} Story"
    
    def whenpublished(self):

        now = timezone.now()
        diff = now-self.created_at

        if diff.days == 0 and diff.seconds >= 0 and diff.seconds < 60:
            seconds = diff.seconds

            if seconds == 1:
                return str(seconds) + "second ago"
            else:
                return str(seconds) + " seconds ago"
            
        if diff.days == 0 and diff.seconds >= 60 and diff.seconds < 3600 :
            minutes = math.floor(diff.seconds/60)
             
            if minutes == 1:
                return str(minutes) + " minute ago"
            
            else:
                return str(minutes) + " minutes ago"
            
        if diff.days == 0 and diff.seconds >= 3600 and diff.seconds < 86400 :
            hours = math.floor(diff.seconds/3600)

            if hours == 1:
                return str(hours) + " hour ago"
            else:
                return str(hours) + " hours ago"
            
        if diff.days >= 1 and diff.days < 30:
            days = diff.days

            if days == 1:
                return str(days) + " day ago"
            else:
                return str(days) + " days ago"
            
        if diff.days >= 30 and diff.days < 365:
            months = math.floor(diff.days/30)

            if months == 1:
                return str(months) + " month ago" 
            else:
                return str(months) + " months ago"
            
        if diff.days >= 365:
            years = math.floor(diff.days/365)

            if years == 1:
                return str(years) + " year ago"
            
            else:
                return str(years) + " years ago"
            
class ChatRoom(models.Model):
    user1 = models.ForeignKey(InstaUser,on_delete=models.CASCADE,related_name="user_1_chat")
    user2 = models.ForeignKey(InstaUser,on_delete=models.CASCADE,related_name="user_2_chat",null=True,blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

class Message(models.Model):
    chat_room = models.ForeignKey(ChatRoom,on_delete=models.CASCADE,related_name="chatroom")
    sender_id = models.ForeignKey(InstaUser,on_delete=models.CASCADE,related_name="senderby",null=True,blank=True)
    text_message = models.CharField(max_length=100)
    image = models.FileField(null=True,blank=True)
    video = models.FileField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True) 



