from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from .restapis import get_dealers_from_cf, get_dealer_reviews_from_cf, post_request
from .models import CarModel
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import requests
import logging
import json
from .models import CarModel

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
def about(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/about.html', context)


# Create a `contact` view to return a static contact page
def contact(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/contact.html', context)

# Create a `login_request` view to handle sign in request
def login_request(request):
    context = {}
    if request.method == "POST":
        # Get username and password from request.POST dictionary
        username = request.POST['username']
        password = request.POST['psw']
        # Try to check if provide credential can be authenticated
        user = authenticate(username=username, password=password)
        if user is not None:
            # If user is valid, call login method to login current user
            login(request, user)
            return redirect('djangoapp:index')
        else:
            # If not, return to login page again
            context["message"]="Username or password is incorrect."
            return redirect('djangoapp:index')
    else:
        return render(request, 'djangoapp/index.html', context)
    

# Create a `logout_request` view to handle sign out request
def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

# Create a `registration_request` view to handle sign up request
def registration_request(request):
    context = {}
    # If it is a GET request, just render the registration page
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    # If it is a POST request
    elif request.method == 'POST':
        # Get user information from request.POST
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            # Check if user already exists
            User.objects.get(username=username)
            user_exist = True
        except:
            # If not, simply log this is a new user
            logger.debug("{} is new user".format(username))
        # If it is a new user
        if not user_exist:
            # Create user in auth_user table
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            # Login the user and redirect to course list page
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context["message"]="Account could not be created try again."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        context = {}
        url = "https://21d1f6fd.us-south.apigw.appdomain.cloud/api/dealership"
        # Get dealers from the URL
        context = {"dealerships": get_dealers_from_cf(url)}
        # Concat all dealer's short name
        # Return a list of dealer short name
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render the reviews of a dealer
# def get_dealer_details(request, dealer_id):
# ...
def get_dealer_details(request, dealer_id):
    context = {}
    parameters = {'dealership': dealer_id}
    url = "https://21d1f6fd.us-south.apigw.appdomain.cloud/api/review"
    #print(dealer_id)
    # Get dealers from the URL
    dealer_details = get_dealer_reviews_from_cf(url,kwargs = parameters)
    context["reviews"]=dealer_details
    return render(request, 'djangoapp/dealer_details.html', context)
# Create a `add_review` view to submit a review
# def add_review(request, dealer_id):
# ...
def add_review(request, dealer_id):
    context = {}
    dealer_url = "https://21d1f6fd.us-south.apigw.appdomain.cloud/api/dealership"
    if request.method == 'GET':
        # Get cars for the dealer
        context = {
            "cars": CarModel.objects.filter(dealer_id=dealer_id),
            "dealer_id": dealer_id,
            "dealer_name": get_dealers_from_cf(dealer_url)[dealer_id-1].full_name,
        }
        
        return render(request, 'djangoapp/add_review.html', context)
    elif request.method == 'POST':
        if request.user.is_authenticated:
            username = request.user.username
            print(request.POST)
            payload = dict()
            car_id = request.POST["car"]
            car = CarModel.objects.get(pk=car_id)
            payload["time"] = datetime.utcnow().isoformat()
            payload["name"] = username
            payload["dealership"] = dealer_id
            payload["id"] = dealer_id
            payload["review"] = request.POST["content"]
            payload["purchase"] = False
            if "purchasecheck" in request.POST:
                if request.POST["purchasecheck"] == 'on':
                    payload["purchase"] = True
            payload["purchase_date"] = request.POST["purchasedate"]
            payload["car_make"] = car.car_make.name
            payload["car_model"] = car.car_name
            payload["car_year"] = int(car.car_year.strftime("%Y"))

            new_payload = {}
            new_payload["review"] = payload
            review_post_url = "https://21d1f6fd.us-south.apigw.appdomain.cloud/api/review"
            post_request(review_post_url, new_payload, id=dealer_id)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)