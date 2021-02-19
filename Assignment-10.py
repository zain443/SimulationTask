#!/usr/bin/python
# -*- coding: latin-1 -*-

from heapq import *
from numpy import random


### STATE ##########################################

class State:
    def __init__(self):
        self.green = False
        self.cars = 0

    def is_green(self):
        """
        True if the light is green
        """
        return self.green

    def add_car(self):
        """
        Adds a car in the queue
        """
        self.cars = self.cars + 1

    def purge_cars(self):
        """
        Empty waiting cars
        """
        self.cars = 0

    def waiting_cars(self):
        """
        Returns the number of car waiting
        """
        return self.cars

    def turn_green(self):
        """
        The light turns green
        """
        self.green = True

    def turn_red(self):
        """
        The light turns red
        """
        self.green = False

    def __str__(self):
        """
        Displays the status of the crossroads
        """
        return "Green light =" + str(self.green) + ", cars=" + str(self.cars)


### EVENTS ###########################################

Tc = 30  # Time latency to change the traffic lights from red to green once a car is found waiting in the queue
Tp = 10  # Passage time


class Event:
    def __init__(self,t,name):
        self.t=t
        self.name=name
    def time(self,t):
        """
        Returns the time at which the event will be processed
        """
        return self.t

    def __str__(self):
        """
        Displays Event
        """
        return self.name + "(" + str(self.t) + ")"

    def __lt__(self, other):
        """
        Compares the event with another sorted by processing order priority
        """
        return self.t < other.t


class CAR(Event):
    def __init__(self, time):
        self.t = time
        self.name = "CAR"

    def action(self, queue, state):
        # fill the code below
        if(state.waiting_cars() == 0):
         queue.insert(G2R(self.t + Tc))
        state.add_car()


class R2G(Event):
    def __init__(self, time):
        self.t = time
        self.name = "R2G"

    def action(self, queue, state):
        # fill the code below
        state.turn_green()
        queue.insert(G2R(self.t + Tp * state.waiting_cars()))


class G2R(Event):
    def __init__(self, time):
        self.t = time
        self.name = "G2R"

    def action(self, queue, state):
        # fill the code below
        state.turn_red()
        state.purge_cars()


### EVENT QUEUE ##############################################

class EventQueue:
    def __init__(self):
        self.q = []

    def notEmpty(self):
        """
      Returns true if the queue is not empty
      """
        return len(self.q) > 0

    def remaining(self):
        """
      Returns the number of events awaiting processing
      """
        return len(self.q)

    def insert(self, event):
        """
      Create a new event in the queue
      """
        heappush(self.q, event)

    def next(self):
        """
      Returns and removes from the queue the next event to be processed
      """
        return heappop(self.q)


### MAIN #####################################################

Q = EventQueue()

Q.insert(CAR(10))
Q.insert(CAR(25))
Q.insert(CAR(35))
Q.insert(CAR(60))
Q.insert(CAR(75))

# For advanced sim , uncomment these lines and change the value of Tp to 15
# random.seed(1)
# additionalNumCarInQueue=100
# tRandom = 80
# for i in range(1, additionalNumCarInQueue):
#    tRandom = random.randint(tRandom+1, tRandom+10)
#    Q.insert( CAR(tRandom) )  


S = State()

# Processing events until the queue is Q is empty
while Q.notEmpty():
    e = heappop(Q.q)
    print(e)
    e.action(Q, S)
