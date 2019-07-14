from django.shortcuts import render
import pyrebase # CC: imported pyrebase wrapper, essentially derives from firebase July 9, 2019
from django.contrib import auth

# CC: Included API from Verve-Slug-Tutor and succesfully integrated authentication ------------------------------------------
config = {
    'apiKey': "AIzaSyBHHg2e5gRop8tcO2RReu8paiEXJbGomVw",
    'authDomain': "verve-slug-tutor.firebaseapp.com",
    'databaseURL': "https://verve-slug-tutor.firebaseio.com",
    'projectId': "verve-slug-tutor",
    'storageBucket': "verve-slug-tutor.appspot.com",
    'messagingSenderId': "1013220996189",
    'appId': "1:1013220996189:web:462bd852caeea191"
  }

firebase = pyrebase.initialize_app(config) # enables the pyrebase wrapper to be used, passed API into function
authe = firebase.auth()
database= firebase.database() # created the database

#CC:  End of API ----------------------------------------------------------------------------------------------------------------

posts = [
    {
        'author': 'Brian Alegria',
        'title': 'Tutoring Post 1',
        'content': 'I need tutoring in advanced physica 8A and I am excellent web dev',
        'date_posted': 'June 30th, 2019'
    },
    {
        'author': 'Another User',
        'title': 'Tutoring Post 2',
        'content': 'Second Post Content',
        'date_posted': 'June 30th, 2019'
    }

]

def home(request):
    context = {
    'posts': posts
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})

def signup(request):
   # Sun 11:23
    name=request.POST.get('name')
    name2=request.POST.get('name2')
    email=request.POST.get('email')
    contact=request.POST.get('contact')
    passw=request.POST.get('pass')

    user=authe.create_user_with_email_and_password(email,passw)
    session_id=user['idToken']
    # CC: Here we create account
    uid = user['localId']
    # CC unique ID for the user

    data = {"name":name, "lastname":name2, "email":email, "contact":contact, "id":uid}
    # to push the data into the database, 1 means account is enabled
    # from above name and email from form and enabled the account
    # database constructor with multiple users
    database.child("users").child(uid).child("details").set(data,session_id)
    return render(request,"blog/signup.html")

def login(request):
    email=request.POST.get('email')
    passw = request.POST.get("pass")
    try: 
        user = authe.sign_in_with_email_and_password(email,passw)
    except:
        message = "invalid credentials"
        return render(request,"blog/login.html",{"messg":message})

    print(user['idToken'])
    session_id=user['idToken']
    request.session['uid']=str(session_id)
    return render(request, "blog/knowledge.html",{"e":email})

def contact(request):
    return render(request, "contact.html", {'title': {'Contact'}})

def knowledge(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("ID Token: "+ str(a))
    try:
        database.child('users').child(a).child('details').child('id').set(a,idtoken)
        name = database.child('users').child(a).child('details').child('id').get(idtoken).val()
        return render(request, 'blog/knowledge.html', {'e':name})
    except KeyError:
        message="Opps! User Logged Out!"
        return render(request,"login.html",{"messg":message})

def profile(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    print("ID Token: "+ str(a))
    try:
        database.child('users').child(a).child('details').child('id').set(a,idtoken)
        #name = database.child('users').child(a).child('details').child('id').get().val()
        name = database.child('users').child(a).child('details').child('id').get(idtoken).val()
        return render(request, 'blog/profile.html', {"e":name})
    except KeyError:
        message =  "Opps! User Logged Out!"
        return render(request,"login.html",{"messg":message})

def logout(request):
    idtoken = request.session['uid']
    a = authe.get_account_info(idtoken)
    a = a['users']
    a = a[0]
    a = a['localId']
    try:
        del a
    except KeyError:
        pass
    return render(request,'blog/login.html')

#def check(request):
 #   idtoken = request.session['uid']
  #  a = authe.get_account_info(idtoken)
   # a = a['users']
   # a = a[0]
   # a = a['localId']
   # information = database.child('users').child(a).('details').child('contact').child('email').child('id').child('lastname').child('name').shallow().get().val()
   # listTime=[] #Help to get all the data
    #for i in information:
    #    listTime.append(i)

    #listTime.sort(reverse=True)
    #print(information)
    #return render(request,'check.html')

# CC: from print down --------------------------------------------------------------------------------------------------------------
