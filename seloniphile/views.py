from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import *
from django.contrib.auth.hashers import make_password,check_password

# Create your views here.
def checkLoggin(view_function):
    def wrapper(request,*args,**kwargs):
        if "email" in request.session:
            try:
                uid = InstaUser.objects.get(email = request.session['email'])
                request.uid = uid 
                return view_function(request,*args,**kwargs)
            except InstaUser.DoesNotExist:
                return redirect("login")
        return redirect("login")
    
    return wrapper

@checkLoggin
def home(request):
    uid = request.uid
    # post_all = instapost.objects.all().order_by('-created_at')

    my_following_users = FollowUserd.objects.filter(following=uid).values_list("following_person",flat=True)

    post_all = instapost.objects.filter(user__in = list(my_following_users) + [uid.id]).order_by("-created_at")

    post_count = instapost.objects.filter(user=uid).count()

    followers = FollowUserd.objects.filter(following_person=uid).count()

    following = FollowUserd.objects.filter(following=uid).count()

    suggested_users = InstaUser.objects.exclude(id__in=list(my_following_users) + [uid.id])[:5]

    reels = CreateReel.objects.all().order_by('-created_at')

    following_story = CreateStory.objects.filter(user_id__in = my_following_users).order_by("-created_at")

    print(reels)    
    print(reels.count())
    
    context = {
         'following' : following,
         'followers' : followers,
         'post_count' : post_count,
         'uid' : uid,
         'post_all' : post_all,
         'suggested_users' : suggested_users,
         "reels" : reels,
         "following_story" : following_story
    }

    return render(request,"seloniphile/home.html",context)

@checkLoggin
def create(request):
    uid = request.uid

    if request.POST:
                uid = InstaUser.objects.get(email = request.session['email'])
                image = request.FILES['image']
                caption = request.POST['caption']
                location = request.POST['location']

                instapost.objects.create(
                    user = uid,
                    image = image,
                    caption = caption,
                    location = location,
                )
                return redirect("home")
    context = {
         "uid" : uid
    }
    return render(request,'seloniphile/create.html',context)

@checkLoggin
def edit_profile(request):
    if "email" in request.session:
            uid = InstaUser.objects.get(email = request.session['email'])  

            if request.POST:
                uid.username = request.POST['username']
                uid.name = request.POST['name']
                uid.bio = request.POST['bio']
                uid.link = request.POST['link']
                uid.description = request.POST['description']

                if "profile_pic" in request.FILES:
                                uid.profile_pic = request.FILES['profile_pic']
                
                uid.save()

            context = {
                        "uid" : uid
                    }
            return render(request,"seloniphile/edit_profile.html",context)
    return render(request,"seloniphile/edit_profile.html")

@checkLoggin
def explore(request):
    if "email" in request.session:
        uid = InstaUser.objects.get(email = request.session['email'])

        following = FollowUserd.objects.filter(
            following=uid
        ).values_list("following_id", flat=True)

        posts = instapost.objects.exclude(user_id__in=following).exclude(user=uid).order_by("?")

        return render(request,"seloniphile/explore.html",{"posts":posts})

def login(request):
    if request.POST:
        email = request.POST['email']
        password =request.POST['password']

        try:
            uid = InstaUser.objects.get(email = email)
            if not check_password(password,uid.password):
                context = {
                    'e_msg' : "Invalid Credentials !"
                }
                return render(request,'seloniphile/login.html',context)
            else:
                request.session['email'] = email 
                context = { 'uid' : uid }
                print("----------->>> home",uid)
                return redirect("home")

        except:
            context = {
                'e_msg' : "User Not Found !"
            }
            return render(request,'seloniphile/login.html',context)

    return render(request,'seloniphile/login.html')

@checkLoggin
def messages(request):
    uid = request.uid

    context = {
         "uid" : uid
    }
    return render(request,'seloniphile/messages.html',context)

@checkLoggin
def notifications(request):
    uid = request.uid

    all_notification = Notification.objects.filter(reciever = uid).order_by("-created_at")
    my_following = FollowUserd.objects.filter(following = uid).values_list("following_person",flat=True)

    context = {
         "uid" : uid,
         "all_notification" : all_notification,
         "my_following"  : my_following
    }
    return render(request,'seloniphile/notifications.html',context)

@checkLoggin
def profile(request):
     if "email" in request.session:
        uid = InstaUser.objects.get(email = request.session['email'])  
        posts = instapost.objects.filter(user=uid)

        post_count = instapost.objects.filter(user=uid).count()

        followers = FollowUserd.objects.filter(following_person=uid).count()

        following = FollowUserd.objects.filter(following_person=uid).count()

        total_likes = LikeUnlike.objects.filter(post_fk__user=uid).count()

        reels = CreateReel.objects.filter(user = uid)

        context = {
                'following' : following,
                'followers' : followers,
                'post_count' : post_count,
                "posts" : posts,
                "uid" : uid,
                "total_likes" : total_likes,
                "reels" : reels,
            }
        return render(request,'seloniphile/profile.html',context)

@checkLoggin   
def reels(request):
    uid = request.uid

    reels = CreateReel.objects.all()

    context = {
         "reels" : reels,
         "uid" : uid
    }
    return render(request,'seloniphile/reels.html',context)

def register(request):
    if request.POST:
        username = request.POST['username']
        email = request.POST['email']
        gender = request.POST['gender']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if InstaUser.objects.filter(username=username).exists():
            context = {
                'e_msg' : "Username Already exists !"
            }
            return render(request,"seloniphile/register.html",context)

        elif InstaUser.objects.filter(email = email).exists():
            context = {
                'e_msg' : "Email Already exists !"
            }
            return render(request,"seloniphile/register.html",context)

        elif password != confirm_password:
            context = {
                'e_msg': "Password does not match !"
            }
            return render(request,"seloniphile/register.html",context)

        else:
            if gender == "male":
                img = "images/boy.png"
            elif gender == "female":
                img = "images/girl.png"
            else :
                 img = "images/boy.png"

            InstaUser.objects.create(
                    username = username,
                    email = email,
                    password = make_password(password),
                    profile_pic = img,
                    gender = gender
                    )
                    
            return redirect("login")
    return render(request,'seloniphile/register.html')

@checkLoggin
def search(request):
     uid = request.uid

     users = []

     if request.method == "POST":
          
          search = request.POST.get("search")

          users = InstaUser.objects.filter(username__icontains=search)
     return render(request,"seloniphile/search.html",{"users":users})

@checkLoggin
def settings(request):
    uid = request.uid

    context = {
         "uid" : uid
    }
    return render(request,'seloniphile/settings.html',context)

@checkLoggin
def followers(request):
     uid = request.uid

     followers_list = FollowUserd.objects.filter(following_person=uid)
     my_following = FollowUserd.objects.filter(following=uid).values_list("following_person_id",flat=True)

     context = {
          "uid" : uid,
          "followers_list" : followers_list,
          "my_following" : my_following
     }

     return render(request,'seloniphile/followers.html',context)

@checkLoggin
def following(request):
    uid = request.uid
    users = InstaUser.objects.exclude(username = uid.username)

    my_following = FollowUserd.objects.filter(following=uid).values_list("following_person_id",flat=True)
    context = {
        "uid" : uid,
        "users" : users,
        "my_following" : my_following
    }
    return render(request,'seloniphile/following.html',context)

@checkLoggin
def follow_unfollow(request,pk):
     uid = request.uid
     target_user = InstaUser.objects.get(id = pk)

     follow_person = FollowUserd.objects.filter(following = uid,following_person = target_user).first()
     
     if follow_person:
          print("unfollow logic")
          follow_person.delete()
     else:
          FollowUserd.objects.create(following = uid,
                following_person = target_user)
          
          Notification.objects.create(
               sender = uid,
               reciever = target_user,
               message = "started following you.",
               notification_type = "follow"
          )
     return redirect('following')

@checkLoggin
def remove_followers(request,pk):
    uid = request.uid

    FollowUserd.objects.filter(id = pk,following_person = uid).delete()

    return redirect("followers")

def logout(request):
    del request.session['email']
    return redirect("login")

@checkLoggin
def Like_Unlike(request,pk):
    uid = request.uid
    post_id = instapost.objects.get(id = pk)

    like = LikeUnlike.objects.filter(user_fk = uid,post_fk = post_id).first()

    if like:
        like.delete()
    else:
        LikeUnlike.objects.create(user_fk=uid,post_fk=post_id)
        if post_id.user != uid:
            Notification.objects.create(
                sender = uid,
                reciever = post_id.user,
                message = "liked your post.",
                notification_type = "like",
                post_fk  = post_id 
            )
    return redirect("home")

@checkLoggin
def comment_post(request,pk):
    uid = request.uid

    print("METHOD =", request.method)
    print("POST DATA =", request.POST)

    if request.method == "POST" : 
        post_id = instapost.objects.get(id=pk)

        
        comment = request.POST['comment']

        print(comment)

        obj = Comment.objects.create(
            user_fk=uid,
            post_fk=post_id,
            comment=comment
        )

        if post_id.user != uid:
            Notification.objects.create(
                sender = uid,
                reciever = post_id.user,
                message = "comment your post.",
                notification_type = "comment",
                post_fk  = post_id 
            )

        print(obj.id)

    return redirect("home")

@checkLoggin
def reel_create(request):
    uid = request.uid

    print("METHOD =", request.method)

    if request.method == "POST":

        print("POST HIT")

        video = request.FILES['video']
        caption = request.POST['caption']
        location = request.POST['location']

        obj = CreateReel.objects.create(
            user=uid,
            video=video,
            caption=caption,
            location = location
        )

        print("REEL SAVED =", obj.id)

        return redirect("reels")
    else:
         return render(request,"seloniphile/reel-create.html",{"uid":uid})

@checkLoggin
def create_story(request):
    uid = request.uid

    if request.method == "POST":
         
         story_caption = request.POST['story_caption']
         story_image = request.FILES['story_image']

         story = CreateStory.objects.create(
              user = uid,
              story_caption = story_caption,
              story_image = story_image                    
            )
         
         return redirect("home")


    return render(request,"seloniphile/create_story.html")

@checkLoggin
def view_story(request,user_id):
     uid = request.uid

     v_story = CreateStory.objects.filter(user_id = user_id).order_by("-created_at")

     context = {
          "v_story" : v_story
     }

     return render(request,"seloniphile/view_stoy.html",context)

@checkLoggin
def user_profile(request,id):
     if "email" in request.session:
        uid = InstaUser.objects.get(id = id)  
        posts = instapost.objects.filter(user=uid)

        post_count = instapost.objects.filter(user=uid).count()

        followers = FollowUserd.objects.filter(following_person=uid).count()

        following = FollowUserd.objects.filter(following_person=uid).count()

        total_likes = LikeUnlike.objects.filter(post_fk__user=uid).count()

        reels = CreateReel.objects.filter(user = uid)

        context = {
                'following' : following,
                'followers' : followers,
                'post_count' : post_count,
                "posts" : posts,
                "uid" : uid,
                "total_likes" : total_likes,
                "reels" : reels,
            }
        return render(request,'seloniphile/profile.html',context)
     
     


