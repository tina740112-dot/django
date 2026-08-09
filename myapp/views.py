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
    import random
    numbers=[]
    for i in range (6):
        lotto1=random.randint(1,42)
        numbers.append(lotto1)
    return render(request, 'lotto1.html', {'numbers': numbers})


def lotto2(request):
    import random

    groups = []
    for i in range(6):
        # 從 1 到 42 中，隨機抽出 6 個「不重複」的數字，並從小到大排序
        numbers = sorted(random.sample(range(1, 43), 6))
        groups.append(numbers)

    return render(request, 'lotto2.html', {'groups': groups})