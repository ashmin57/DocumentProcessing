from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# Create your views here.


@login_required(login_url='login')
def HomePage(request):
    return render(request, 'home.html')


def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        if pass1 != pass2:
            return HttpResponse("Your password is not matched")
        else:
            my_user = User.objects.create_user(uname, email, pass1)
            my_user.save()
        return redirect('login')

    return render(request, 'signup.html')


def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        pass1 = request.POST.get('pass')
        user = authenticate(request, username=username, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return HttpResponse('Username or Password is incorrect')

    return render(request, 'login.html')


def LogoutPage(request):
    logout(request)
    return redirect('login')


def ProfilePage(request):
    return render(request, 'profile.html')


def NewFilePage(request):
    return render(request, 'newFile.html')


def ExtractedDataPage(request):
    return render(request, 'extractedData.html')


def handle_file_upload(request):
    if request.method == 'POST':
        file = request.FILES['fileInput']
        # Process the file as needed (e.g., save it to a specific location)
        # You can access the file data using 'file.read()' or save it to disk using 'file.save(file_path)'
        # Determine the file type (image or pdf) based on the file extension
        file_extension = file.name.split('.')[-1].lower()
        if file_extension in ['jpg', 'jpeg', 'png', 'gif']:
            file_type = 'image'
        elif file_extension == 'pdf':
            file_type = 'pdf'
        else:
            file_type = None

        # Set the file_url and file_type variables to pass to the template
        if file_type:
            # Assuming the uploaded file is saved to MEDIA_ROOT/uploads/
            file_url = f"/media/uploads/{file.name}"
            return render(request, 'newFile.html', {'file_url': file_url, 'file_type': file_type})
        else:
            # Handle unsupported file types
            return render(request, 'newFile.html', {'error': 'Unsupported file type.'})

    return render(request, 'newFile.html')
