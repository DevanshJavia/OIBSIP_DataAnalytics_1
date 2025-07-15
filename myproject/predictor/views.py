from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import HousePriceForm
from .models import PredictionHistory
import joblib
import pandas as pd
import json
from django.core.serializers.json import DjangoJSONEncoder
import shap
import numpy as np
import matplotlib.pyplot as plt
import os

# Load the trained model
model = joblib.load('model/model.pkl')

# Load background data for SHAP explainer (use part of training data or mock sample)
background_data = pd.read_csv("/Users/devanshjavia/Desktop/Proj/Predicting House Prices with Linear Regression copy/Housing.csv.xls")  # Update the path
background_data = background_data.drop(columns=['price'])

# SHAP Explainer setup
explainer = shap.Explainer(model.predict, background_data)

# =================== AUTH ===================

def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('login')


# =================== PAGES ===================

@login_required
def home(request):
    predicted_price = None
    shap_values = None
    feature_names = []
    feature_contributions = []

    if request.method == 'POST':
        form = HousePriceForm(request.POST)
        if form.is_valid():
            data = pd.DataFrame([form.cleaned_data])
            predicted_price = model.predict(data)[0]
            predicted_price = round(predicted_price, 2)

            # Save prediction
            PredictionHistory.objects.create(
                user=request.user,
                predicted_price=predicted_price,
                **form.cleaned_data
            )

            # SHAP Explanation
            shap_result = explainer(data)
            shap_values = shap_result.values[0]
            feature_names = data.columns.tolist()
            feature_contributions = list(zip(feature_names, shap_values))

    else:
        form = HousePriceForm()

    return render(request, 'home.html', {
        'form': form,
        'predicted_price': predicted_price,
        'feature_contributions': feature_contributions
    })


@login_required
def predict(request):
    predicted_price = None
    if request.method == 'POST':
        form = HousePriceForm(request.POST)
        if form.is_valid():
            data = pd.DataFrame([form.cleaned_data])
            predicted_price = model.predict(data)[0]
            predicted_price = round(predicted_price, 2)

            # Save prediction
            PredictionHistory.objects.create(
                user=request.user,
                predicted_price=predicted_price,
                **form.cleaned_data
            )
    else:
        form = HousePriceForm()

    return render(request, 'predict.html', {
        'form': form,
        'predicted_price': predicted_price
    })


@login_required
def dashboard(request):
    history = PredictionHistory.objects.filter(user=request.user).order_by('timestamp')
    avg_price = history.aggregate(Avg('predicted_price'))['predicted_price__avg'] or 0
    total_predictions = history.count()

    # Prepare data for charts
    history_data = list(history.values('timestamp', 'predicted_price', 'furnishingstatus'))
    history_json = json.dumps(history_data, cls=DjangoJSONEncoder)

    # SHAP Summary Plot - once and saved
    try:
        if not os.path.exists('static/images/shap_summary.png'):
            shap_values = explainer(background_data)
            shap.plots.beeswarm(shap_values, max_display=15, show=False)
            os.makedirs('static/images', exist_ok=True)
            plt.tight_layout()
            plt.savefig('static/images/shap_summary.png')
            plt.close()
    except Exception as e:
        print("SHAP summary plot error:", e)

    return render(request, 'dashboard.html', {
        'history': history,
        'avg_price': round(avg_price, 2),
        'total_predictions': total_predictions,
        'history_json': history_json,
    })


def about_view(request):
    return render(request, 'about.html')


def shap_plot_view(request):
    return render(request, 'shap_plot.html')  # shows shap_summary.png
