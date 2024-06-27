# fastVoyages

fastVoyages is a web application that helps users manage and plan their travels efficiently.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Environment Variables](#environment-variables)

## Installation

To get started with fastVoyages, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/AdrianeRuggiero/fastVoyages.git
   cd fastVoyages

2. Create a virtual environment and activate it:
    ```bash
    python3 -m venv venv
    source venv/bin/activate

3. Install the dependencies:
    ```bash
    pip install -r requirements.txt

## Usage

To run the application locally, follow these steps:

1. Ensure that you have set up your environment variables (see Environment Variables section).

2. Start the backend server:
    ```bash
    python registration.py

3. Navigate to http://127.0.0.1:5000 in your web browser.

## Environment Variables

Create a .env file in the root directory of your project and add the following environment variables:
    ```bash 
    CLIENT_ID='your_client_id'
    CLIENT_SECRET='your_client_secret'
    OPENCAGE_API_KEY='your_opencage_api_key'

