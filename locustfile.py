from locust import HttpUser, TaskSet, task, between
from bs4 import BeautifulSoup
from dotenv import load_dotenv
import os

load_dotenv()

class UserBehavior(TaskSet):

    def on_start(self):
        """Perform login at the start of the test."""
        self.register_and_login()

    def register_and_login(self):
        """Register and login to the application."""
        self.register()
        self.login()

    def register(self):
        """Register a new user."""
        register_response = self.client.post("/register", data={
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-01",
            "country_of_residence": "USA",
            "email": "lesia.kapliuk@ecoles-epsi.net",
            "password": "password123"
        })
        
        print(f"Register response status code: {register_response.status_code}")
        print(f"Register response content: {register_response.content.decode('utf-8')}")

        if register_response.status_code == 200:
            print("Registration successful")
        elif register_response.status_code == 400 and "Email already registered" in register_response.json().get("message", ""):
            print("Email already registered")
        else:
            print(f"Registration failed: {register_response.status_code}, {register_response.text}")

    def login(self):
        """Login to the application."""
        login_response = self.client.post("/login", data={
            "email": "lesia.kapliuk@ecoles-epsi.net",
            "password": "password123"
        })

        if login_response.status_code == 200:
            print("Login successful")
        else:
            print(f"Login failed: {login_response.status_code}, {login_response.text}")

    @task(1)
    def home(self):
        """Access the home page."""
        response = self.client.get("/")
        if response.status_code == 200:
            print("Home page accessed successfully")
        else:
            print(f"Failed to access home page: {response.status_code}, {response.text}")

    @task(2)
    def flight_search(self):
        """Perform a flight search."""
        flight_response = self.client.post("/flight_search_results", data={
            "origin": "NYC",
            "max_price": "500",
            "departure_date": "2024-07-01",
            "return_date": "2024-07-15",
            "one_way": "on",
            "non_stop": "on"
        })

        if flight_response.status_code == 200:
            print("Flight search successful")
        else:
            print(f"Flight search failed: {flight_response.status_code}, {flight_response.text}")

class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 9)
