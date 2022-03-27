from ast import Str
from email import message
from multiprocessing import context
from django.shortcuts import render ,HttpResponse , redirect
from . models import uploadfile , Orders
import requests
import os
import PyPDF2
import razorpay
from Hello.settings import RAZORPAY_API_KEY,RAZORPAY_API_SECRET_KEY
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


path = r"media"
Fpath = None
dir_list = None
d= None

client = razorpay.Client(auth=(RAZORPAY_API_KEY, RAZORPAY_API_SECRET_KEY))


# Create your views here.
def index(request):
    
    return render(request,'index.html')

def about(request):
    
    return render(request,'about.html')

def send_files(request):
    global Fpath , name , payment_order_id ,printC,printT , id_o , z , campus
    if request.method =="POST" :
        name = request.POST.get("name")
        myfile = request.FILES.getlist("uploadfiles")
        campus = request.POST.get("campus")
        PrintingType = request.POST.get("PrintingType")
        PrintingColor = request.POST.get("PrintingColor")
        
        
        if PrintingType == "2" :
            printT = "Double-sided"
        else:
            printT = "Single-sided"
        print("------------",printT)

        if PrintingColor == "2" :
            printC = "Colour"
        else:
            printC = "Black-White"



        file_list = []
        # print(myfile)
        # print(name,"this is campus",name)
    
        for f in myfile:
            new_file = uploadfile(f_name=name, myfiles=f, campus_name= campus )
            new_file.save()
            file_list.append(new_file.myfiles.url)
       
        #send file to telegram
        if campus == '1':
            campus = "HKBk College of Engineering"
            # dir_list = os.listdir(path)[0]
            # Fpath = os.path.join(path, dir_list)
            c= file_list[0]
            z= c[7:]
            d= c[-4:]
            print("file path",z)
            print("file type",d)  
            Fpath = os.path.join(path, z)            
            if d == ".jpg":
                page = 1
                cost = (page * 2)
                
                # file = {'photo':open(Fpath,'rb')}
                # resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendPhoto?chat_id=-621048814&caption={}'.format(name),files=file)
                # print(resp.status_code)

            elif d == ".png":
                page = 1
                cost = (page * 2)
                
                # file = {'photo':open(Fpath,'rb')}
                # resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendPhoto?chat_id=-621048814&caption={}'.format(name),files=file)
                # print(resp.status_code)
            elif d == "jpeg":
                page = 1
                cost = (page * 2)
                

            elif d == ".pdf":

                pdfFileObj = open(Fpath, 'rb')
                pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
                page = pdfReader.numPages  # page number
                # get totalnumber of pages and page numbering in PyPDF2 starts with 0
                pageObj = pdfReader.getPage(0)
                pageObj.extractText()
                pdfFileObj.close()
                cost = (page * 2)
                type = '.pdf'
                print(page)
                # file = {'document':open(Fpath,'rb')}
                # resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendDocument?chat_id=-621048814&caption={}'.format(name),files=file)
                # print(resp.status_code)
               

            else:
                
                messages.error(request," Only '.jpg' '.png' '.pdf' files are allowed")
                return redirect('/')



            
            DATA = {
            "amount": 100*cost,
            "currency": "INR",
            "receipt": z[0][0],

            }
            
            
            


        
            # server order
            order = client.order.create(data=DATA)
            payment_order_id = order['id']
            #orders database 
            order_db = Orders(name= name,campus=campus,paymentorder_id= payment_order_id,items_json=z)
            order_db.save()
            id_o =order_db.order_id


            
            return render(request,'about.html',{'new_url': file_list , 'page':page ,'cost': cost , "file_name":z ,'api_key':RAZORPAY_API_KEY,'order_id': payment_order_id})
        else:
            messages.error(request, ' Please select Campus')
            return redirect('/')
            

def payment(request):
    
    
    print(Fpath)
    
    d= Fpath[-4:]
    response = request.POST
    params_dict = {
        'razorpay_payment_id' : response['razorpay_payment_id'],
        'razorpay_order_id': response['razorpay_order_id'],
        'razorpay_signature': response['razorpay_signature'],
    }
    

    # create a Razorpay Client instance
    try:
        status = client.utility.verify_payment_signature(params_dict)
        # print('this is response.......', response)
        # print("--------",d)
        #comment on file
        file_id = [id_o, printT , printC , name]

        mess = "Thanks , your order is getting ready. Order id : ", id_o 
        
        if d == ".jpg" or d== "jpeg":
            file = {'photo':open(Fpath,'rb')}
            resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendPhoto?chat_id=-621048814&caption={}'.format(file_id),files=file)
            print(resp.status_code)
            messages.success(request,mess)
            return redirect('/', {'status': True})
        elif d == ".png":                
            file = {'photo':open(Fpath,'rb')}
            resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendPhoto?chat_id=-621048814&caption={}'.format(file_id),files=file)
            print(resp.status_code)
            messages.success(request,mess)
            return redirect('/', {'status': True})

        elif d == ".pdf":

            pdfFileObj = open(Fpath, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            page = pdfReader.numPages  # page number
            # get totalnumber of pages and page numbering in PyPDF2 starts with 0
            pageObj = pdfReader.getPage(0)
            pageObj.extractText()
            pdfFileObj.close()
            
            #print(page)
            file = {'document':open(Fpath,'rb')}
            resp = requests.post('https://api.telegram.org/bot5179242020:AAH9IukRSGWFbUiWVFDUJSYhCuzj2NAuHG8/sendDocument?chat_id=-621048814&caption={}'.format(file_id),files=file)
            print(resp.status_code)
            messages.success(request,mess)
            return redirect('/', {'status': True})


        else:
            return render(request, 'Index.html', {'status': False})     
     

    

    
    except:
        return render(request, 'help.html', {'status': False})     
     

def handleSignup(request):

    if request.method == 'POST':
        # Get the Post parameters
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        # check for errorneousinput
        if len(username) > 10:
            messages.error(request, "Username must be under 10 characters")

            return redirect('/')
        if not username.isalnum():  

            return redirect('/')
            
        if pass1 != pass2:
            messages.error(request, "please check your password")
            return redirect('/')
        



        #creat user
        myuser = User.objects.create_user(username, email, pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.save()
        messages.success(request,"Your zeroXnow account has been successfully created . Please Login ")
        return redirect('/')

    else:
        return HttpResponse("404 - Not Found")

def handleLogin(request):
    if request.method == 'POST':
        # Get the Post parameters
        loginusername = request.POST['loginusername']
        
        loginpass = request.POST['logpass']
        user = authenticate(username=loginusername, password=loginpass)

        if user is not None:
            login(request, user)
            messages.success(request, 'Successfully Logged in')

            return redirect('/')
            
        else:
            messages.error(request, 'Invalid Credentials, Please Try again')
            return redirect('/')
            


    return HttpResponse("handleLogin")

def handleLogout(request):
    
    logout(request)
    messages.success(request, 'Successfully Logged Out')
    return redirect('/')



def handelOrder(request):
    

    return render(request, 'order.html')        