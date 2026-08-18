from unicodedata import name

from django.shortcuts import render
from django.http import HttpResponse


def sayhello(request):
    return HttpResponse("<b>Hello World 40!!!!!</b>")

def hello1(request,username):
    print(username)
    return HttpResponse(f"<b>Hello {username}!!!!!</b>")
  
from datetime import datetime
def hello2(request,username):
    print(f'username:{username}')#print username
    now = datetime.now()#make time now
    print(f'now:{now}')#print time now
    # return HttpResponse('Hello')
    return render(request,'hello2.html',locals())#將變數傳給模板
def hello3(request,username):
    print(f'username:{username}')#print username
    now_dt = datetime.now()#make time now
    now = f"民國{now_dt.year - 1911}年{now_dt.month:02d}月{now_dt.day:02d}日 {now_dt.hour:02d}:{now_dt.minute:02d}:{now_dt.second:02d}"
    print(f'now:{now}')#print time now
    # return HttpResponse('Hello')
    return render(request,'hello3.html',locals())#將變數傳給模板
    
def hello4(request, username1, username2):
    # print(username1)
    # print(username2)
    return HttpResponse("Hello "+ username1 + " "+username2)
  
import random

def dicel(request):
    no1 = random.randint(1,6)
    no2 = random.randint(1,6)
    no3 = random.randint(1,6)
    print(f'no1:{no1}, no2:{no2}, no3:{no3}')
    #return render(request, 'dice1.html', locals())#將變數傳給模板
    return render(request, 'dice1.html', {'no1': no1, 'no2': no2, 'no3': no3})#將變數傳給模板，跟上面的寫法一樣，是正統的寫法
  
def dice2(request):
  student = {'id':1234,'name':'john','sex':'male'}
  fruits= ['apple','banana','orange']
  print(f'student:{student}, fruits:{fruits}')
  return render(request, 'dice2.html', {'student': student, 'fruits': fruits})

def dice3(request):
  person1 ={'name':'amy','age':18,'phone':'0912345678'}
  person2 ={'name':'bob','age':20,'phone':'0987654321'}
  person3 ={'name':'cathy','age':22,'phone':'0922333444'}
  persons = [person1, person2, person3]
  print(persons)
# return HttpResponse("Hello,dice3")
  persons=[]#模擬無資料
  return render(request, 'dice3.html', {'persons': persons})

def lotto1(request):
    num_list = random.sample(range(1,6), 5)
    print(num_list)
  
    return render(request, 'lotto1.html', locals())
  
def lotto2(request):
    random_num_lists=[]
    for i in range(1,7):
      num_list=random.sample(range(1,43), 6) 
      #print(num_list)
      num_list=sorted(num_list)#sort the list
      random_num_lists.append(num_list)
      print(random_num_lists)
    return render(request, 'lotto2.html', locals())
  
from django.shortcuts import render

def get1(request):
   # name=request.GET['name']
   #city=request.GET['city']
   #basic-07.py
   #透過get()方法
    name = request.GET.get('name',None) #如果沒有name參數，則預設為"no name"
    city = request.GET.get('city',None) #若沒有city參數，則預設為"no city"
    print(f'name:{name}, city:{city}')
   # return HttpResponse("hello,get1")
    return render(request, 'get1.html', {'name': name, 'city': city})
 
def get2(request):
    try:
        name = request.GET['name']
        city = request.GET['city']
        status = True
        print(f'name:{name}, city:{city}')
    except:
        status = False
    print(f'status:{status}')
    return render(request, 'get2.html', locals())
  
def get3(request, mode):
    print(f'mode:{mode}')
    if mode =='save':
        username=request.GET.get('username',None)
        password=request.GET.get('password',None) 
        print(f'username:{username}, password:{password}')
        
        password ='*'*(len(password) - 3) + password[-3:]
        return render(request, 'get3.html', locals())
        
    elif mode =='load':
            return render(request, 'get3.html', locals())

def post1(request):
    if request.method == 'POST':
        username = request.POST.get('username', None).strip()#去除前後空白
        password = request.POST.get('password', None).strip()#去除前後空白
        print(f'username:{username}, password:{password}')
        if username == 'admin' and password == '123456':
            #return HttpResponse('登入成功')
            status = True

        else:
           # return HttpResponse('登入失敗')
            status = False
        return render(request, 'post1_response.html', {'status': status, 'username': username})
    else:
        # return render('hello post1')
        return render(request, 'post1.html',locals())
    
def post2(request):
  if request.method=='POST':
    items=request.POST.getlist('items',None)
    print(items)
    #return HttpResponse("送出資料")
    return render(request, 'post2_response.html', locals())
  else:
    return render(request, 'post2.html', locals())
def homework3(request):
    
    return render('hello home3')
  