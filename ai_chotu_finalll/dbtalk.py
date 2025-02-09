import mysql.connector
import json
import requests
from datetime import date
from decimal import Decimal
from groq import Groq

# Function to convert date and Decimal objects to string
def serialize_dates(obj):
    if isinstance(obj, date):
        return obj.isoformat()  # Convert date to ISO format string
    elif isinstance(obj, Decimal):
        return float(obj)  # Convert Decimal to float
    raise TypeError(f'Object of type {obj.__class__.__name__} is not JSON serializable')

def fetch_and_query_product_data(user_query):
    # Database configuration
    db_config = {
        'host': 'localhost',  # or '127.0.0.1'
        'user': 'root',       # default username for XAMPP
        'password': '',       # default password for XAMPP
        'database': 'ai chotu'  # your database name
    }

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch product details
    cursor.execute("SELECT * FROM product_detail")
    product_data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    # Prepare data for Groq AI
    formatted_data = json.dumps(product_data, default=serialize_dates)

    # Groq AI integration
    client = Groq(api_key="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")

    # Prepare the payload for the API request
    completion = client.chat.completions.create(
        model="llama-3.1-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": f"Here is the product data from the database: {formatted_data}. Please answer questions based on this data."
            },
            {
                "role": "user",
                "content": user_query
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the response
    response = ""
    for chunk in completion:
        response += chunk.choices[0].delta.content or ""

    return response