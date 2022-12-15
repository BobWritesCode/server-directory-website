from django.shortcuts import render

# Create your views here.
def get_directory_list(request):
    return render(request , 'directory/directory_list.html')
