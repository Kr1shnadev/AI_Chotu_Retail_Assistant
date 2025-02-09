import streamlit as st
import cv2
import mysql.connector
from PIL import Image
from pyzbar.pyzbar import decode
from datetime import date


# Connect to the MySQL database
mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="ai chotu"
)

# Create a cursor object
mycursor = mydb.cursor()
current_date=date.today()

def scan_barcode():
    # Capture video from the default camera
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    
    if ret:
        cv2.imwrite('captured_image.png', frame)
        
        # Convert the frame to a PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        
        st.image(pil_image)  # Display the captured image in Streamlit
        st.success("Image captured successfully!")
        
        image_path = "captured_image.png"
        image = Image.open(image_path)

        # Decode the barcode
        decoded_objects = decode(image)

        # Display the decoded information
        if decoded_objects:
            for obj in decoded_objects:
                data = obj.data.decode("utf-8")
                st.write("Data:", data)

                # Check if a barcode was detected
                if data:
                    product_no = int(data)

                    # Search for the product in the database
                    mycursor.execute("SELECT * FROM product_detail WHERE Product_No = %s", (product_no,))
                    result = mycursor.fetchone()
                    cap.release()
                    # Check if the product exists
                    if result:
                        st.success("Product Found!")
                        st.write("Product No:", result[1])
                        st.write("Product Name:", result[2])
                        st.write("MFD:", result[3])
                        st.write("EFD:", result[4])
                        st.write("Quantity:", result[5])
                        st.write("Price:", result[6])
                        st.write("Lot_Price:", result[7])
                        st.write("Category:", result[8])
                        if current_date >= result[4]:
                            st.warning("The product is expired")
                        else:
                            st.success("The product is not expired")
                        

                        # Update the product sales
                        mycursor.execute("UPDATE product_detail SET Quantity = Quantity - 1 WHERE Product_No = %s", (product_no,))
                        mydb.commit()
                        st.success("Product Sales Updated!")
                    else:
                        st.warning("Product Not Found!")
                        #add_product_form(product_no)
        else:
            st.warning("No barcodes found in the image.")
    else:
        st.error("Error: Could not read frame.")

    # Release the capture
    cap.release()

def bcod():
# Streamlit interface
    st.title("Barcode Scanner")
    if st.button("Scan Barcode"):
        scan_barcode()

    # Close the database connection when the app stops
    if st.button("Close Database Connection"):
        mycursor.close()
        mydb.close()
        st.success("Database connection closed.")
if __name__ == "__main__":
    bcod()