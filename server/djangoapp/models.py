from django.db import models
from django.utils.timezone import now


# Create your models here.

# <HINT> Create a Car Make model `class CarMake(models.Model)`:
# - Name
# - Description
# - Any other fields you would like to include in car make model
# - __str__ method to print a car make object
class CarMake(models.Model):
    name = models.CharField(null = False, max_length = 300)
    description = models.CharField(null = False, max_length = 300)
    id = models.BigAutoField(primary_key = True)

    def __str__(self):
        return self.name
# <HINT> Create a Car Model model `class CarModel(models.Model):`:
# - Many-To-One relationship to Car Make model (One Car Make has many Car Models, using ForeignKey field)
# - Name
# - Dealer id, used to refer a dealer created in cloudant database
# - Type (CharField with a choices argument to provide limited choices such as Sedan, SUV, WAGON, etc.)
# - Year (DateField)
# - Any other fields you would like to include in car model
# - __str__ method to print a car make object
class CarModel(models.Model):
    TYPES = (
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("PICKUP", "Pickup"), ("MOTORCYCLE", "Motorcycle"), ("MUSCLE", "Muscle"), ("SPORT", "Sport"), ("OTHER", "Other")
        )
    id = models.BigAutoField(primary_key = True)
    car_make = models.ForeignKey(CarMake, on_delete=models.CASCADE)
    car_name = models.CharField(null=False, max_length=30)
    car_type = models.CharField(max_length=30, choices=TYPES)
    dealer_id = models.IntegerField()
    car_year = models.DateField()

    def __str__(self):
        return "Name: " + self.car_name + \
                " Make Name: "+ self.car_make.name + \
                " Type: " + self.car_type + \
                " Dealer ID: " + str(self.dealer_id)+ \
                " Year: " + str(self.car_year)
# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:

    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name

# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, review, purchase_date, car_make, car_model, car_year,sentiment, id):
        self.dealership=dealership
        self.name=name
        self.purchase=purchase
        self.review=review
        self.purchase_date=purchase_date
        self.car_make=car_make
        self.car_model=car_model
        self.car_year=car_year
        self.sentiment=sentiment #Watson NLU service
        self.id=id

    def __str__(self):
        return "Review: " + self.review + " Sentiment: " + str(self.sentiment['sentiment']['document']['label']) 
