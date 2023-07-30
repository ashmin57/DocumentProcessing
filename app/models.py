from django.contrib.auth.models import User
from django.db import models
import tensorflow as tf
import os

model_file = 'invoiceresumemodel.h5'
model_path = os.path.join(os.path.dirname(__file__), 'models', model_file)


# Check if the file exists
if not os.path.isfile(model_path):
    raise FileNotFoundError(f"Model file not found at: {model_path}")

# Load the model
model = tf.keras.models.load_model(model_path)


class Document(models.Model):
    file = models.FileField(upload_to='documents/')
    upload_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
