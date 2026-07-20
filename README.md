<h1 align="center">AutoOracle AI </h1>

<p align="center">
  <strong>A Premium, Full-Stack Machine Learning Pipeline & Web Application for predicting used car prices.</strong><br>
  <em>(Tailored for the Sri Lankan Automotive Market)</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
  <img src="https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB" alt="React">
  <img src="https://img.shields.io/badge/Vite-B73BFE?style=for-the-badge&logo=vite&logoColor=FFD62E" alt="Vite">
</p>

---

## 📖 Project Overview
**AutoOracle AI** is an end-to-end Machine Learning system designed to accurately estimate the fair market selling price of used cars. It calculates the intrinsic value of a vehicle based on its original ex-showroom price and applies complex, AI-driven depreciation factors based on age, mileage, fuel type, and transmission.

### 🇱🇰 Sri Lankan Market Adaptation
The data and models in this repository have been specifically calibrated for the **Sri Lankan market**. Historical vehicle data was scaled to account for the unique economic factors in Sri Lanka, including high import vehicle taxes (often 3x-4x base value) and LKR currency conversion rates, ensuring the predictions are highly realistic for local users.

---

## 🏗️ Full System Architecture

The project is split into three distinct layers:
1. **Machine Learning Pipeline:** Data preprocessing and model training.
2. **Backend API:** A REST API that serves the trained AI model.
3. **Frontend UI:** A cinematic, premium React web application.

```mermaid
graph TD
    subgraph "1. Machine Learning Pipeline (Jupyter)"
        A[(Raw Car Dataset<br>car_data_sl.csv)] --> B[Data Preprocessing & Encoding]
        B --> C[Feature Selection]
        C --> D[Random Forest Regressor]
        D -->|Exports| E([car_prediction_model_sl.pkl])
    end

    subgraph "2. Backend Server (Python / FastAPI)"
        E -.->|Loads Model| F[api.py]
        F -->|Exposes Endpoint| G["/predict POST API"]
    end

    subgraph "3. Frontend Web App (React + Vite)"
        H[Cinematic Hero Section] --> I[Multi-Step Input Form]
        I -->|Sends JSON Request| G
        G -->|Returns Valuation Data| J[Results Dashboard]
        J --> K[Interactive Gauge & Charts]
    end

    style A fill:#f9f,stroke:#333,stroke-width:2px
    style E fill:#f39c12,stroke:#333,stroke-width:2px
    style F fill:#2ecc71,stroke:#333,stroke-width:2px
    style J fill:#3498db,stroke:#333,stroke-width:2px
```

---

## 🧠 How the AI Works

Unlike standard prediction models that rely on the vehicle's name (which causes issues with new, unseen cars), **AutoOracle AI relies entirely on the vehicle's "Current Ex-Showroom Price"**. 

1. **The Baseline:** The Ex-Showroom price acts as the ultimate proxy for the car's tier, luxury level, and brand value. 
2. **The Depreciation Engine:** The Random Forest algorithm uses the remaining features (Age, Kilometers Driven, Fuel Type, Transmission, Previous Owners) as complex **depreciation factors**.
3. **The Result:** By subtracting the AI-calculated depreciation from the baseline price, the model can accurately predict the value of *any* car in the world, even if that specific model wasn't in the training dataset!

---

## 💻 Installation & Setup Instructions

To run the full stack locally, you need two terminals: one for the Python Backend, and one for the React Frontend.

### Prerequisites
- Python 3.8+
- Node.js (v18 or higher)

### Step 1: Clone the Repository
```bash
git clone https://github.com/SihanUdayaratna03/AutoOracle-AI.git
cd AutoOracle-AI
```

### Step 2: Start the FastAPI Backend
Open your first terminal and run:
```bash
# Optional: Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python requirements
pip install -r requirements.txt
pip install fastapi uvicorn

# Start the API server
python api.py
```
*The backend will now be running on `http://localhost:8000`*

### Step 3: Start the React + Vite Frontend
Open a **second, separate terminal** and run:
```bash
# Navigate into the frontend directory
cd car-ui

# Install Node modules
npm install

# Start the Vite development server
npm run dev
```
*The stunning frontend UI will now be accessible in your browser at `http://localhost:5173`!*

---

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
