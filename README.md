# 🛒 Retail Virtual Assistant  

An AI-powered **retail management assistant** designed to help shop owners **track inventory, monitor product expiry, and analyze sales trends**. This assistant also supports **voice commands** for hands-free management.  

## ✨ Features  
- **📦 Inventory Tracking** – Monitors stock and updates quantity after sales.  
- **⏳ Expiry Date Management** – Notifies about expired or soon-to-expire products.  
- **📊 Sales Insights & Predictions** – Uses machine learning to forecast demand.  
- **🎙 Voice Commands** – Allows hands-free interaction.  
- **📈 Data Visualization** – Displays sales trends using interactive charts.  
- **🔍 Barcode Scanning** – Retrieves product details using a scanner.  

## 🚀 Tech Stack  
- **Backend:** Python, FastAPI  
- **Frontend:** Streamlit  
- **Database:** MySQL  
- **AI/ML:** NLP for voice interaction, RandomForest for sales prediction  
- **Libraries:** OpenCV, Pyzbar, SpeechRecognition, gTTS, Plotly  

## 📂 Project Structure  
📁 retail-assistant
├── ai_chotu.py # Main multi-page Streamlit app
├── main.py # Voice command interface & AI responses
├── chart.py # Sales visualization & forecasting
├── bcode.py # Barcode scanner for product lookup
├── dbtalk.py # Database interaction with AI query handling
├── sqlquery.py # AI-generated SQL query execution
├── tst.py # Speech recognition test script
└── README.md # Project documentation

## 🔧 Installation  
1. Clone the repository:  
   ```bash
   git clone https://github.com/yourusername/retail-assistant.git  
   cd retail-assistant  
❗❗❗❗To Run the assistant:
             streamlit run ai_chotu.py  
