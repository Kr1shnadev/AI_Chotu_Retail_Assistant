import mysql.connector
from groq import Groq

def execute_sql_query(user_input):
    # Initialize Groq client
    client = Groq(api_key="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")

    # Generate SQL query using Groq AI
    completion = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {
                "role": "system",
                "content": "whatever i say next should be converted to sql query only (no comments or suggestions)and take an example database  ai chotu and tables namely product_detail and saletrack .these are the columns in product_detail table : Sl_No, Product_No, Product_Name, MFD, EFD, Quantity, Price, Lot_Price, Category . And for saletrack table : Sl_No, Date_of_Purchase, No_of_Item_Sold, Date_of_Item_Sold, Payment_Method . Only give the query and nothing else!"
            },
            {
                "role": "user",
                "content": user_input
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        stream=True,
        stop=None,
    )

    # Collect the generated SQL query
    sql_query = ""
    for chunk in completion:
        sql_query += chunk.choices[0].delta.content or ""

    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'ai chotu'
    }

    # Connect to the database and execute the SQL query
    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor()

    try:
        cursor.execute(sql_query)
        connection.commit()  # Commit the changes to the database
        result = "Query executed successfully."
    except mysql.connector.Error as err:
        result = f"Error: {err}"
    finally:
        cursor.close()  # Close the cursor
        connection.close()  # Close the connection

    return result
