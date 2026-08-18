from django.shortcuts import render

def homework3(request):
    if request.method == 'POST':
        name = request.POST.get('username', '')
        gender = request.POST.get('gender', '')
        hobbies = request.POST.getlist('hobby')

        # 判斷性別稱謂
        if gender == '男':
            title = '先生您好！'
        elif gender == '女':
            title = '小姐您好！'
        else:
            title = '您好！'

        context = {
            'name': name,
            'title': title,
            'hobbies': hobbies,
        }
        # 這裡改為你截圖中的檔名 homework3_result.html
        return render(request, 'homework3_result.html', context)

    return render(request, 'homework3.html')