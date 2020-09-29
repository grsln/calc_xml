import os
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from .calc_time import calc_file


# страница выбора и загрузки файла
def index(request):
    if request.method == "POST":
        if 'file' in request.FILES:
            file = request.FILES["file"]
            fs = FileSystemStorage()
            filename = fs.save(os.path.join('uploads', file.name), file)
            file_url = fs.url(filename)
            return render(request, 'calc_time/calc.html', {'file_url': file_url})
    return render(request, 'calc_time/index.html')


# страница ввода интервала дат и имени
def calc(request):
    if request.method == "POST":
        file_url = request.POST['file_url']
        start = None
        end = None
        fullname = None
        if 'date-cb' in request.POST:
            start = request.POST['start-date']
            end = request.POST['end-date']
        if 'fullname-cb' in request.POST:
            fullname = request.POST['fullname']
        result = calc_file(file_url, start=start, end=end, fullname=fullname)
        return render(request, 'calc_time/result.html', {'result': result})
    return render(request, 'calc_time/calc.html')
