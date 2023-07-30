from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
import os
from django.http import FileResponse
from django.conf import settings
from .models import Document
import cv2
import numpy as np
import tensorflow as tf


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

        # Check if the file type is allowed (jpg, jpeg, or png)
        allowed_types = ['jpg', 'jpeg', 'png']
        file_extension = file.name.split('.')[-1].lower()
        if file_extension not in allowed_types:
            return render(request, 'newFile.html', {'error': 'Unsupported file type.'})

        # Save the uploaded file
        document = Document(file=file, user=request.user)
        document.save()

        # Preprocess the uploaded image and make predictions
        prediction = classify_image_with_model(document.file.path)

        # Pass the prediction and the file path to the template
        return render(request, 'newFile.html', {'prediction': prediction, 'file_path': document.file.url})

    return render(request, 'newFile.html')


def preprocess_image(image_path):
    # Load the image using OpenCV
    image = cv2.imread(image_path)

    # Resize the image if needed
    desired_width, desired_height = 224, 224
    resized_image = cv2.resize(image, (desired_width, desired_height))

    # Normalize the pixel values to be within [0, 1]
    normalized_image = resized_image.astype(np.float32) / 255.0

    # Convert the image to a Keras-compatible format
    processed_image = np.expand_dims(normalized_image, axis=0)

    return processed_image


def classify_image_with_model(image_path):
    # Load the model
    model_file = 'invoiceresumemodel.h5'
    model_path = os.path.join(os.path.dirname(__file__), 'models', model_file)
    model = tf.keras.models.load_model(model_path)
    # Preprocess the image
    preprocessed_image = preprocess_image(image_path)

    # Make predictions
    prediction = model.predict(preprocessed_image)

    # You may need to further process the prediction depending on your model output
    return prediction


def download_extracted_data(request):
    # Path to the extracted CSV file
    extracted_data_path = os.path.join(
        settings.MEDIA_ROOT, 'extracted_data.csv')

    # Open the file in binary mode
    with open(extracted_data_path, 'rb') as file:
        # Create a FileResponse object
        response = FileResponse(file)
        # Set the content type for the response
        response['Content-Type'] = 'text/csv'
        # Set the content disposition to force download
        response['Content-Disposition'] = 'attachment; filename="extracted_data.csv"'

    return response
