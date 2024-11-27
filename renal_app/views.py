import pickle
import sklearn
import pandas as pd
from .models import PatientTest 
from django.shortcuts import render,redirect,HttpResponse, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from .models import Profile
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.decorators import user_passes_test
from .form import MedicationForm
import json
from django.http import JsonResponse
from collections import defaultdict
def load_model():
    with open('static/random_forest_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

# Function to predict chronic disease
def chronic_prediction(model, input_values):
    feature_names = ['age', 'blood_pressure', 'specific_gravity', 'albumin', 'sugar',
                     'red_blood_cells', 'pus_cell', 'pus_cell_clumps', 'bacteria',
                     'blood_glucose_random', 'blood_urea', 'serum_creatinine', 'sodium',
                     'potassium', 'haemoglobin', 'packed_cell_volume',
                     'white_blood_cell_count', 'red_blood_cell_count', 'hypertension',
                     'diabetes_mellitus', 'coronary_artery_disease', 'appetite',
                     'peda_edema', 'aanemia']
    input_data = pd.DataFrame([input_values], columns=feature_names)
    result = model.predict(input_data)
    if result[0] == 0:
        recommendation = 'No chronic disease detected. Maintain a healthy lifestyle and regular check-ups.'
    else:
        recommendation = 'Chronic disease detected. Please consult a doctor for a comprehensive treatment plan.'
    
    return recommendation
    # return 'The person does not have a chronic disease.' if result[0] == 0 else 'The person has a chronic disease.'


def home(request):
    return render(request , 'Index.html')

def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        useremail = request.POST.get('useremail')
        role = request.POST.get('role')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')
        image = request.FILES.get('image')

        # Check if any field is empty
        if not all([username, useremail, role, password, confpassword]):
            messages.error(request, "All fields are required!")
            return redirect('register')

        # Check if passwords match
        if password != confpassword:
            messages.error(request, "Your password and confirm password are not the same!")
            return redirect('register')

        try:
            # Create User
            user = User.objects.create_user(username=username, email=useremail, password=password)

            # Create Profile
            Profile.objects.create(user=user, role=role, image=image)

            messages.success(request, "Registration successful! Please log in.")
            return redirect('user_login')
        except IntegrityError:
            messages.error(request, "Username already taken. Please choose another one.")
            return redirect('register')

    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        useremail = request.POST.get('email')
        password = request.POST.get('password')

        try:
            # Get the user by email
            user = User.objects.get(email=useremail)
        except User.DoesNotExist:
            user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)

            if user is not None:
                login(request, user)

                # Get the user's profile to check the role
                try:
                    profile = Profile.objects.get(user=user)
                    role = profile.role

                    redirect_to = request.GET.get('next', '/')
                    if role == 'doctor':
                        return redirect(redirect_to if redirect_to else 'doctor_dashboard') 
                    elif role == 'patient':
                        return redirect(redirect_to if redirect_to else 'patient_dashboard')
                    else:
                        messages.error(request, "Role is not defined.")
                        return redirect('user_login')

                except Profile.DoesNotExist:
                    messages.error(request, "Profile not found.")
                    return redirect('user_login')

            else:
                messages.error(request, "Invalid password.")
                return redirect('user_login')
        else:
            messages.error(request, "Invalid email or password.")
            return redirect('user_login')

    return render(request , 'login.html')

def is_patient(user):
    return user.profile.role == 'patient'

def is_doctor(user):
    return user.profile.role == 'doctor'


@login_required
@user_passes_test(is_doctor)
def doctor_dashboard_view(request):
    user_profile = get_object_or_404(Profile, user=request.user, role='doctor')
    total_tests = PatientTest.objects.count()
    positive_message = 'The person has a chronic disease.'
    negative_message = 'The person does not have a chronic disease.'

    # Count of positive and negative predictions
    positive_tests = PatientTest.objects.filter( prediction=positive_message).count()
    negative_tests = PatientTest.objects.filter( prediction=negative_message).count()


    if total_tests > 0:
        positive_percentage = (positive_tests / total_tests) * 100
        negative_percentage = (negative_tests / total_tests) * 100
    else:
        positive_percentage = 0
        negative_percentage = 0

    context = {
        'profile': user_profile,
        'total_tests': total_tests,
        'positive_tests': positive_tests,
        'negative_tests': negative_tests,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
    }
    return render(request, 'doctor_dashboard.html', context)

@login_required
@user_passes_test(is_patient)
def patient_dashboard_view(request):
    user_profile = get_object_or_404(Profile, user=request.user, role='patient')
    # Define the exact messages used in the chronic_prediction function
    positive_message = 'The person has a chronic disease.'
    negative_message = 'The person does not have a chronic disease.'

    total_tests = PatientTest.objects.filter(profile=user_profile).count()
    positive_tests = PatientTest.objects.filter(profile=user_profile, prediction=positive_message).count()
    negative_tests = PatientTest.objects.filter(profile=user_profile, prediction=negative_message).count()

    # Calculate percentages (ensure no division by zero)
    if total_tests > 0:
        positive_percentage = (positive_tests / total_tests) * 100
        negative_percentage = (negative_tests / total_tests) * 100
    else:
        positive_percentage = 0
        negative_percentage = 0

    context = {
        'profile': user_profile,
        'total_tests': total_tests,
        'positive_tests': positive_tests,
        'negative_tests': negative_tests,
        'positive_percentage': positive_percentage,
        'negative_percentage': negative_percentage,
    }

    return render(request, 'patient_dashboard.html' ,context )

#patient Pages 
def patinetTest(request):
    user_profile = get_object_or_404(Profile, user=request.user, role='patient')
    if request.method == 'POST':
        # Extract form data from request.POST
        input_values = [
            float(request.POST.get('age')),
            float(request.POST.get('blood_pressure')),
            float(request.POST.get('specific_gravity')),
            float(request.POST.get('albumin')),
            float(request.POST.get('sugar')),
            float(request.POST.get('red_blood_cells')),
            float(request.POST.get('pus_cell')),
            float(request.POST.get('pus_cell_clumps')),
            float(request.POST.get('bacteria')),
            float(request.POST.get('blood_glucose_random')),
            float(request.POST.get('blood_urea')),
            float(request.POST.get('serum_creatinine')),
            float(request.POST.get('sodium')),
            float(request.POST.get('potassium')),
            float(request.POST.get('haemoglobin')),
            float(request.POST.get('packed_cell_volume')),
            float(request.POST.get('white_blood_cell_count')),
            float(request.POST.get('red_blood_cell_count')),
            float(request.POST.get('hypertension')),
            float(request.POST.get('diabetes_mellitus')),
            float(request.POST.get('coronary_artery_disease')),
            float(request.POST.get('appetite')),
            float(request.POST.get('peda_edema')),
            float(request.POST.get('aanemia')),
        ]

         # Get the current logged-in user's profile
        profile = Profile.objects.get(user=request.user)
      
        model = load_model()
        prediction = chronic_prediction(model, input_values)
        # Generate recommendation based on the prediction
        recommendation = chronic_prediction(model, input_values)

        # Save the form data and prediction to the database
        PatientTest.objects.create(
            profile=profile,
            age=input_values[0],
            blood_pressure=input_values[1],
            specific_gravity=input_values[2],
            albumin=input_values[3],
            sugar=input_values[4],
            red_blood_cells=input_values[5],
            pus_cell=input_values[6],
            pus_cell_clumps=input_values[7],
            bacteria=input_values[8],
            blood_glucose_random=input_values[9],
            blood_urea=input_values[10],
            serum_creatinine=input_values[11],
            sodium=input_values[12],
            potassium=input_values[13],
            haemoglobin=input_values[14],
            packed_cell_volume=input_values[15],
            white_blood_cell_count=input_values[16],
            red_blood_cell_count=input_values[17],
            hypertension=input_values[18],
            diabetes_mellitus=input_values[19],
            coronary_artery_disease=input_values[20],
            appetite=input_values[21],
            pedal_edema=input_values[22],
            anemia=input_values[23],
            prediction=prediction,
            recommendation=recommendation
        )
        user_profile = get_object_or_404(Profile, user=request.user, role='patient')
        context = {
        'profile': user_profile,
        'prediction': prediction,
        'recommendation': recommendation
       }
        return render(request, 'Presult.html', context)
    else:
        context = {
        'profile': user_profile
       }
        return render(request, 'PTest.html',context)
    
def user_logout(request):
    auth_logout(request)
    redirect_to = request.GET.get('next', 'user_login')
    return redirect(redirect_to)


def Presults(request):
     return render(request, 'Presult.html')
def Preport(request):
    if not request.user.is_authenticated:
        return redirect('login')  # Redirect to login if the user is not authenticated
    user_profile = get_object_or_404(Profile, user=request.user, role='patient')
    patient_tests = PatientTest.objects.filter(profile=user_profile)
    context = {
        'profile': user_profile,
        'patient_tests': patient_tests,
       }
    return render(request, 'Preport.html',context)

def disease_progression(request):
    user_profile = get_object_or_404(Profile, user=request.user, role='patient')
    profile = get_object_or_404(Profile, user=request.user)
    tests = PatientTest.objects.filter(profile=profile).order_by('-timestamp')
   # Mapping for prediction strings to numeric values
    prediction_mapping = {
        'The person does not have a chronic disease.': 0,
        'The person has a chronic disease.': 1,
        # Add more mappings if needed
    }

    # Initialize defaultdict to handle missing keys with a default value
    grouped_data = defaultdict(lambda: {'predictions': [], 'recommendations': set(), 'ages': []})

    for test in tests:
        date_key = test.timestamp.strftime('%Y-%m-%d')
        
        # Convert string predictions to numeric using the mapping
        numeric_prediction = prediction_mapping.get(test.prediction, None)
        
        if numeric_prediction is not None:
            grouped_data[date_key]['predictions'].append(numeric_prediction)
        
        grouped_data[date_key]['recommendations'].add(test.recommendation)
        grouped_data[date_key]['ages'].append(test.age)

    # Prepare data for visualization
    dates = []
    avg_predictions = []
    age_brackets = defaultdict(list)
    recommendation_counts = defaultdict(int)

    for date, data in grouped_data.items():
        dates.append(date)
        if data['predictions']:
            avg_predictions.append(sum(data['predictions']) / len(data['predictions']))

        # Age bracket logic
        for age in data['ages']:
            if age <= 20:
                age_brackets['0-20'].append(age)
            elif 21 <= age <= 40:
                age_brackets['21-40'].append(age)
            elif 41 <= age <= 60:
                age_brackets['41-60'].append(age)
            else:
                age_brackets['61+'].append(age)

        # Count recommendations
        for recommendation in data['recommendations']:
            recommendation_counts[recommendation] += 1

    # Average age per bracket
    avg_age_brackets = {k: sum(v)/len(v) for k, v in age_brackets.items()}

    context = {
        'dates': json.dumps(dates),
        'avg_predictions': json.dumps(avg_predictions),
        'avg_age_brackets': json.dumps(avg_age_brackets),
        'recommendation_counts': json.dumps(dict(recommendation_counts)),
        'profile': user_profile,
    }
    return render(request, 'PDiseaseProgression.html', context)

#Docter Pages 
def DAllpaitensReports(request):
    patient_tests = PatientTest.objects.all()
    user_profile = get_object_or_404(Profile, user=request.user, role='doctor')

    if request.method == 'POST':
        test_id = request.POST.get('test_id')
        message = request.POST.get('message')
        if test_id and message:
            test = get_object_or_404(PatientTest, id=test_id)
            test.message = message
            test.message_sent = True
            test.save()
            return redirect('dallpaitensreports')  
    context = {
        'profile': user_profile,
        'patient_tests': patient_tests
    }
    return render(request, 'DAllpaitensReport.html',context)

def OneTimeUser(request):
    context = {}  # Initialize context
    if request.method == 'POST':
        input_values = [
            float(request.POST.get('age')),
            float(request.POST.get('blood_pressure')),
            float(request.POST.get('specific_gravity')),
            float(request.POST.get('albumin')),
            float(request.POST.get('sugar')),
            float(request.POST.get('red_blood_cells')),
            float(request.POST.get('pus_cell')),
            float(request.POST.get('pus_cell_clumps')),
            float(request.POST.get('bacteria')),
            float(request.POST.get('blood_glucose_random')),
            float(request.POST.get('blood_urea')),
            float(request.POST.get('serum_creatinine')),
            float(request.POST.get('sodium')),
            float(request.POST.get('potassium')),
            float(request.POST.get('haemoglobin')),
            float(request.POST.get('packed_cell_volume')),
            float(request.POST.get('white_blood_cell_count')),
            float(request.POST.get('red_blood_cell_count')),
            float(request.POST.get('hypertension')),
            float(request.POST.get('diabetes_mellitus')),
            float(request.POST.get('coronary_artery_disease')),
            float(request.POST.get('appetite')),
            float(request.POST.get('peda_edema')),
            float(request.POST.get('aanemia')),
        ]
        model = load_model()
        prediction = chronic_prediction(model, input_values)
        recommendation = chronic_prediction(model, input_values)
        
        context = {
            'prediction': prediction,
            'recommendation': recommendation
        }
    return render(request, 'OneTimeUser.html',context)



# New SetUp
def deshboard(request):
    
    return render(request, 'dashbaord.html')