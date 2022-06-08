from django.shortcuts import render, HttpResponse

# Create your views here.
def index(request):
    return render(request, "index.html")

def send_files(request):
    if request.method == "POST":
        name = request.POST.get("filename")
        myfile = request.FILES.getlist("uploadfoles")
        print(f"It's my file: {myfile}")    
        return HttpResponse("ok")
