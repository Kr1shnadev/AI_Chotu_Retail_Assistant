import streamlit as st
import mysql.connector
import pandas as pd
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

# Function to fetch product and sales data from the database
def fetch_sales_data():
    # Database configuration
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'database': 'ai chotu'
    }

    # Connect to the database
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    # Fetch product details
    cursor.execute("SELECT * FROM product_detail")
    product_data = cursor.fetchall()

    # Fetch sales data from saletrack table
    cursor.execute("SELECT * FROM saletrack")
    sales_data = cursor.fetchall()

    # Close the database connection
    cursor.close()
    conn.close()

    return pd.DataFrame(product_data), pd.DataFrame(sales_data)

def main():
    # Streamlit app
    st.title("Sales Prediction Dashboard")

    # Step 1: Fetch data
    product_df, sales_df = fetch_sales_data()

    # Display the data
    if st.checkbox("Show Product Data"):
        st.subheader("Product Data")
        st.write(product_df)

    if st.checkbox("Show Sales Data"):
        st.subheader("Sales Data")
        st.write(sales_df)

    # Step 2: Data Preparation
    sales_df['Date_of_Item_Sold'] = pd.to_datetime(sales_df['Date_of_Item_Sold'])
    sales_df['month'] = sales_df['Date_of_Item_Sold'].dt.month
    sales_df['year'] = sales_df['Date_of_Item_Sold'].dt.year
    sales_df['sales_lag1'] = sales_df['No_of_Item_Sold'].shift(1)
    sales_df['sales_lag2'] = sales_df['No_of_Item_Sold'].shift(2)
    sales_df.dropna(inplace=True)

    # Step 3: Model Selection
    X = sales_df[['month', 'year', 'sales_lag1', 'sales_lag2']]
    y = sales_df['No_of_Item_Sold']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    model = RandomForestRegressor()
    model.fit(X_train, y_train)

    # Step 4: Making Predictions
    predictions = model.predict(X_test)

    # Step 5: Visualization
    results = pd.DataFrame({'Actual': y_test, 'Predicted': predictions})
    results.reset_index(drop=True, inplace=True)

    # Plotting with Plotly
    fig = px.line(results, title='Actual vs Predicted Sales', labels={'index': 'Index', 'value': 'Sales'})
    fig.add_scatter(y=results['Actual'], mode='lines', name='Actual Sales')
    fig.add_scatter(y=results['Predicted'], mode='lines', name='Predicted Sales')
    st.plotly_chart(fig)

    # Step 6: Analyze Sales Data
    sales_summary = sales_df.groupby('Product_No')['No_of_Item_Sold'].sum().reset_index()
    top_product = sales_summary.loc[sales_summary['No_of_Item_Sold'].idxmax()]

    st.subheader("Top Product by Sales")
    st.write(f"Product with the highest sales: Product No: {top_product['Product_No']}, Total Sold: {top_product['No_of_Item_Sold']}")

    # Step 7: Predict next month's sales for each product
    next_month = (sales_df['month'].max() % 12) + 1
    next_year = sales_df['year'].max() + (sales_df['month'].max() // 12)

    next_month_data = pd.DataFrame({
        'month': [next_month] * len(product_df),
        'year': [next_year] * len(product_df),
        'sales_lag1': [0] * len(product_df),
        'sales_lag2': [0] * len(product_df)
    })

    predicted_sales = model.predict(next_month_data)

    predicted_sales_df = product_df[['Product_No', 'Product_Name']].copy()
    predicted_sales_df['Predicted_Sales'] = predicted_sales

    top_predicted_product = predicted_sales_df.loc[predicted_sales_df['Predicted_Sales'].idxmax()]

    st.subheader("Predicted Product for Next Month")
    st.write(f"Predicted product with the highest sales next month: Product No: {top_predicted_product['Product_No']}, Product Name: {top_predicted_product['Product_Name']}, Predicted Sales: {top_predicted_product['Predicted_Sales']}")
if __name__ == "__main__":
    main()