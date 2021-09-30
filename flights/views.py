from django.shortcuts import render
from .models import Flight, Airport, Passenger # import db objects
from django.urls import reverse
from django.http import HttpResponseRedirect

# Create your views here.
def index(request):
    return render(request, "flights/index.html", {
        "flights": Flight.objects.all()
    })

def flight(request, flight_id):
    flight = Flight.objects.get(id=flight_id)
    passengers = flight.passengers.all()
    non_passengers = Passenger.objects.exclude(flights=flight).all()

    return render(request, "flights/flight.html", {
        "flight": flight,
        "passengers": passengers,
        "non_passengers": non_passengers
    })

def book(request, flight_id):
    # for a post request, add a new flight
    if request.method == "POST":
        # accessing the flight
        flight = Flight.objects.get(pk=flight_id)

        # find passenger id from the submitted form
        passenger_id = int(request.POST["passenger"])

        # find the passenger based on id
        passenger = Passenger.objects.get(pk=passenger_id)

        # add passenger to the flight
        passenger.flights.add(flight)

        # redirect user to flight page
        return HttpResponseRedirect( reverse("flight", args=(flight.id,)))
