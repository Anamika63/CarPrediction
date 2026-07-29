import streamlit as st
import pandas as pd
import pickle

# ------------------------------
# Load Model
# ------------------------------
model = pickle.load(open("model.pkl", "rb"))

# Load Dataset
car_data = pd.read_csv("Cardetails.csv.xls")

# Extract Brand Name
def get_brand_name(car_name):
    return car_name.split(" ")[0]

car_data["name"] = car_data["name"].apply(get_brand_name)

# ------------------------------
# Page Settings
# ------------------------------
st.set_page_config(
    page_title="Car Price Prediction",
    page_icon="🚗",
    layout="centered"
)

st.title("🚗 Car Price Prediction")
st.write("Enter the details below to predict the estimated car price.")

# ------------------------------
# Input Fields
# ------------------------------
name = st.selectbox("Car Brand", sorted(car_data["name"].unique()))

year = st.slider(
    "Manufacturing Year",
    1994,
    2024,
    2018
)

km_driven = st.number_input(
    "Kilometers Driven",
    min_value=0,
    value=50000
)

fuel = st.selectbox(
    "Fuel Type",
    car_data["fuel"].unique()
)

seller_type = st.selectbox(
    "Seller Type",
    car_data["seller_type"].unique()
)

transmission = st.selectbox(
    "Transmission",
    car_data["transmission"].unique()
)

owner = st.selectbox(
    "Owner Type",
    car_data["owner"].unique()
)

mileage = st.number_input(
    "Mileage (km/l)",
    min_value=0.0,
    value=18.0
)

engine = st.number_input(
    "Engine (CC)",
    min_value=500,
    value=1200
)

max_power = st.number_input(
    "Max Power (BHP)",
    min_value=0.0,
    value=80.0
)

seats = st.selectbox(
    "Number of Seats",
    [4, 5, 6, 7, 8, 9, 10]
)

# ------------------------------
# Prediction
# ------------------------------
if st.button("Predict Price"):

    input_data = pd.DataFrame(
        [[
            name,
            year,
            km_driven,
            fuel,
            seller_type,
            transmission,
            owner,
            mileage,
            engine,
            max_power,
            seats
        ]],
        columns=[
            "name",
            "year",
            "km_driven",
            "fuel",
            "seller_type",
            "transmission",
            "owner",
            "mileage",
            "engine",
            "max_power",
            "seats"
        ]
    )

    # Encoding
    input_data["owner"] = input_data["owner"].replace(
        [
            "First Owner",
            "Second Owner",
            "Third Owner",
            "Fourth & Above Owner",
            "Test Drive Car"
        ],
        [1, 2, 3, 4, 5]
    )

    input_data["fuel"] = input_data["fuel"].replace(
        ["Diesel", "Petrol", "LPG", "CNG"],
        [1, 2, 3, 4]
    )

    input_data["seller_type"] = input_data["seller_type"].replace(
        ["Individual", "Dealer", "Trustmark Dealer"],
        [1, 2, 3]
    )

    input_data["transmission"] = input_data["transmission"].replace(
        ["Manual", "Automatic"],
        [1, 2]
    )

    input_data["name"] = input_data["name"].replace(
        [
            "Maruti","Skoda","Honda","Hyundai","Toyota","Ford",
            "Renault","Mahindra","Tata","Chevrolet","Datsun",
            "Jeep","Mercedes-Benz","Mitsubishi","Audi",
            "Volkswagen","BMW","Nissan","Lexus","Jaguar",
            "Land","MG","Volvo","Daewoo","Kia","Fiat",
            "Force","Ambassador","Ashok","Isuzu","Opel"
        ],
        list(range(1, 32))
    )

    prediction = model.predict(input_data)

    st.success(f"Estimated Car Price: ₹ {prediction[0]:,.2f}")