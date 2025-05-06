# Soft Paws Studios - Online Shopping Platform

## Overview

Soft Paws Studios is a fully functional online e-commerce platform specializing in trendy clothing items such as tops, bottoms, dresses, and accessories. Built using Django, HTML, CSS, JavaScript, and MySQL, the platform provides a seamless shopping experience for users, from browsing products to placing orders and leaving feedback.

## Key Features

* **User Authentication:** Secure registration and login functionality for individual user accounts.
* **Product Catalog:** Browse a wide range of products categorized into tops, bottoms, dresses, and accessories.
* **Product Detail View:** Detailed information for each product, including descriptions, images, and pricing.
* **Shopping Cart:** Users can add desired quantities of items to their cart.
* **Cart Management:** Ability to view, update quantities, and remove items from the shopping cart.
* **Secure Checkout:** A streamlined payment process where users can enter their details to complete their purchase.
* **Post-Purchase Review System:** Registered users can leave reviews and ratings for purchased products.

## Technologies Used

* **Backend Framework:** Django (Python)
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MySQL

## Setup and Installation

1.  **Prerequisites:**
    * Python 3.x installed on your system.
    * Django 3.x or higher
    * pip (Python package installer) installed.
    * MySQL server installed and running.
    * JavaScript

2.  **Clone the Repository:**
    ```bash
    git clone <repository_url>
    cd soft_paws_studios
    ```
    *(Replace `<repository_url>` with the actual URL of your project repository)*

3.  **Create a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On macOS/Linux
    venv\Scripts\activate  # On Windows
    ```

4.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Ensure you have a `requirements.txt` file listing all the Django dependencies including the MySQL connector)*

5.  **Configure Database:**
    * Create a MySQL database for the project (e.g., `soft_paws_db`).
    * Open the `settings.py` file in your Django project directory.
    * Configure the `DATABASES` setting to connect to your MySQL database:

    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': 'soft_paws_db',
            'USER': 'your_mysql_username',
            'PASSWORD': 'your_mysql_password',
            'HOST': 'localhost',  # Or your MySQL host
            'PORT': '3306',      # Or your MySQL port
            'OPTIONS': {
                'charset': 'utf8mb4',
            },
        }
    }
    ```
    *(Replace `'soft_paws_db'`, `'your_mysql_username'`, and `'your_mysql_password'` with your actual database credentials)*

6.  **Run Migrations:**
    ```bash
    python manage.py migrate
    ```
    This command creates the necessary database tables.

7.  **Create a Superuser (for admin access):**
    ```bash
    python manage.py createsuperuser
    ```
    Follow the prompts to create an administrator account.

8.  **Run the Development Server:**
    ```bash
    python manage.py runserver
    ```
    Open your web browser and navigate to `http://127.0.0.1:8000/` to access the platform.

## Usage

* **Registration/Login:** New users can register an account, and existing users can log in to access the full features of the platform.
* **Browsing Products:** Navigate through the different categories (Tops, Bottoms, Dresses, Accessories) to view available items.
* **Viewing Product Details:** Click on a product to see its detailed description, images, and price.
* **Adding to Cart:** Select the desired quantity and click "Add to Cart" to place items in your shopping cart.
* **Shopping Cart:** Access your cart to review the selected items, update quantities, or remove items.
* **Checkout:** Proceed to the checkout page to enter your shipping and payment information.
* **Leaving Reviews:** After a successful purchase, logged-in users can leave reviews and ratings for the products they bought.

