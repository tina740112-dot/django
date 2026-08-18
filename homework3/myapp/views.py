from django.shortcuts import render

from django.shortcuts import render

def homework3(request):
    if request.method == 'POST':
        name = request.POST.get('name', '')
        gender = request.POST.get('gender', '')
        hobbies = request.POST.getlist('hobby')
        
        # 判定性別稱謂
        if gender == '男':
            title = '先生'
        elif gender == '女':
            title = '您好'
        else:
            title = '你好'

        context = {
            'name': name,
            'title': title,
            'hobbies': hobbies,
        }
        return render(request, 'homework3.html', context)

    # GET 請求 (第一次載入頁面)
    return render(request, 'homework3.html')
