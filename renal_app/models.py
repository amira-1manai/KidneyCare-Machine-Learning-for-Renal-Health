from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
# Create your models here.
User._meta.get_field('email')._unique = True
class Profile(models.Model):
    ROLE_CHOICES = (
        ('doctor', 'Doctor'),
        ('patient', 'Patient'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    image = models.ImageField(upload_to='profile_images', blank=True, null=True)

    def __str__(self):
        return self.user.username
class PatientTest(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    age = models.FloatField()
    blood_pressure = models.FloatField()
    specific_gravity = models.FloatField()
    albumin = models.FloatField()
    sugar = models.FloatField()
    red_blood_cells = models.IntegerField()
    pus_cell = models.IntegerField()
    pus_cell_clumps = models.IntegerField()
    bacteria = models.IntegerField()
    blood_glucose_random = models.FloatField()
    blood_urea = models.FloatField()
    serum_creatinine = models.FloatField()
    sodium = models.FloatField()
    potassium = models.FloatField()
    haemoglobin = models.FloatField()
    packed_cell_volume = models.FloatField()
    white_blood_cell_count = models.FloatField()
    red_blood_cell_count = models.FloatField()
    hypertension = models.IntegerField()
    diabetes_mellitus = models.IntegerField()
    coronary_artery_disease = models.IntegerField()
    appetite = models.IntegerField()
    pedal_edema = models.IntegerField()
    anemia = models.IntegerField()
    prediction = models.CharField(max_length=255)
    timestamp = models.DateTimeField(default=timezone.now) 
    message = models.TextField(blank=True, null=True)
    message_sent = models.BooleanField(default=False)
    recommendation = models.TextField(blank=True, null=True) 
    def __str__(self):
        return f"Patient Test {self.id} - {self.profile.user.username} - Prediction: {self.prediction}"
    