<h1 align="center">AutoOracle AI 🏎️🔮</h1>

<p align="center">
  <strong>A Machine Learning pipeline for predicting used car prices based on vehicle history, specifications, and market data.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white" alt="Scikit-Learn">
  <img src="https://img.shields.io/badge/Pandas-150458?style=for-the-badge&logo=pandas&logoColor=white" alt="Pandas">
  <img src="https://img.shields.io/badge/Jupyter-F37626?style=for-the-badge&logo=jupyter&logoColor=white" alt="Jupyter">
</p>

---

## 📌 Overview
**AutoOracle AI** is an end-to-end Machine Learning project designed to accurately estimate the selling price of used cars. By analyzing historical vehicle data, the model accounts for factors like depreciation (age), usage (kilometers driven), fuel type, and transmission.

## 🏗️ System Architecture

The following diagram illustrates the data flow and model training pipeline utilized in this project:

```mermaid
graph TD
    A[(Raw Car Dataset<br>CSV)] --> B[Data Preprocessing]
    B --> C{Encoding Categorical Data}
    C -->|Fuel, Transmission, Seller Type| D[Feature Selection]
    
    D --> E[Train / Test Split<br>90% Train, 10% Test]
    
    E --> F[Model Training]
    
    F --> G[Linear Regression]
    F --> H[Lasso Regression]
    F --> I[Random Forest Regressor]
    
    G --> J[Model Evaluation<br>R-Squared Score]
    H --> J
    I --> J
    
    J --> K((Final Prediction<br>Engine))
    
    style A fill:#f9f,stroke:#333,stroke-width:2px
    style K fill:#bbf,stroke:#333,stroke-width:2px
```

## 📊 The Dataset
The model is trained on a robust dataset containing the following features:
* **`Car_Name`**: The specific model of the vehicle.
* **`Year`**: The year the car was purchased.
* **`Selling_Price`**: Target Variable (The price the car sold for).
* **`Present_Price`**: The current ex-showroom price of the car.
* **`Kms_Driven`**: Total distance the car has been driven.
* **`Fuel_Type`**: Petrol, Diesel, or CNG.
* **`Seller_Type`**: Sold by a Dealer or Individual.
* **`Transmission`**: Manual or Automatic.
* **`Owner`**: Number of previous owners.

## 🧠 Models Evaluated
To find the most accurate predictor, multiple regression algorithms were evaluated:
1. **Linear Regression:** Establishes a baseline linear relationship between features and price.
2. **Lasso Regression:** Introduces L1 regularization to penalize less important features and prevent overfitting.
3. **Random Forest Regressor:** An ensemble learning method using multiple decision trees to capture non-linear relationships.

## 🚀 Setup & Installation

### Prerequisites
Make sure you have Python 3.8+ installed on your local machine.

### Installation Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/SihanUdayaratna03/AutoOracle-AI.git
   cd AutoOracle-AI
   ```

2. **Create a virtual environment (Recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Launch the Notebook:**
   ```bash
   jupyter notebook
   ```
   Open `car-price-prediction.ipynb` in your browser to explore the code, train the models, and view the visualizations.

## 📜 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
