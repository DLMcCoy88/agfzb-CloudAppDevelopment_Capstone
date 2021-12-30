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
            ("SEDAN", "Sedan"), ("SUV", "SUV"), ("WAGON", "Wagon"), ("PICKUP", "Pickup"), ("MOTORCYCLE", "Motorcycle")
        )

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


# <HINT> Create a plain Python class `DealerReview` to hold review data
