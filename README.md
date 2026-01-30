# RA Centre Court Reservation Bot

Uses Web automation to automatically book and reserve badminton courts at RA Centre

# How to run the application:
You will need to create a virtual environment and install selenium in order to use it:

$ python -m venv venv

$ source venv/bin/activate

$ pip install selenium

You also need to download Chrome webdriver. You can go to the official Chrome driver website (https://developer.chrome.com/docs/chromedriver/) and download the latest stable release for your operating system. You will end up with a zip file and the zip file will contain a file called “chromedriver”. Put this file in a folder alongside the app.py file and you will be ready to run the application.

# How It Works:

Tech Usedd: Python, Selenium

By using multithreading, the bot starts by opening 2 chrome instances of the RA Centre court booking website through pred-configured credentials in order to book mutliple courts at once. The bot navigates to the next week to ensure booking in advance by a week. This involves simulating clicks and waiting for the web page to load with WebDriverWait to ensure elements are ready for interaction. The bot then checks the court availiablity based off pre-defined conditions such as time-slot, court #, and date, and constantly refreshes the page until the specified courts are availiable. If the desired court is availiable the bot will login using your email and password and add the courts to your cart. A method of payment must be added to the RA Centre website beforehand in order for the program to work. If the payment method is added then the bot will automatically select said payment method and and complete the order.
