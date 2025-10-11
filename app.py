# app.py

import streamlit as st
import pandas as pd
import joblib

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="Prediksi Kepuasan Penumpang Pesawat",
    page_icon="✈️",
    layout="centered",
)

# --- FUNGSI & PEMUATAN MODEL ---
try:
    model = joblib.load('best_airline_satisfaction_model.joblib')
    label_encoder = joblib.load('label_encoder.joblib') 
except FileNotFoundError as e:
    st.error(f"Error: File model atau encoder tidak ditemukan. Pastikan file 'best_airline_satisfaction_model.joblib' dan 'label_encoder.joblib' ada di folder yang sama. Detail: {e}")
    st.stop()

# Fungsi untuk melakukan prediksi (TIDAK BERUBAH)
def predict(data):
    # Buat DataFrame dari input
    df = pd.DataFrame([data])
    
    # Lakukan one-hot encoding manual yang konsisten dengan data training
    cat_features = {
        'Gender': ['Male'],
        'Customer Type': ['disloyal Customer'],
        'Type of Travel': ['Personal Travel'],
        'Class': ['Eco', 'Eco Plus']
    }
    
    # Loop untuk membuat kolom one-hot
    for feature, categories in cat_features.items():
        for category in categories:
            col_name = f"{feature}_{category}"
            # Cek jika nilai input sama dengan kategori target untuk encoding
            df[col_name] = 1 if df[feature].iloc[0] == category else 0
            
    # Hapus kolom kategorikal asli
    df = df.drop(columns=list(cat_features.keys()))

    # Pastikan semua kolom dari model ada di dataframe input
    model_cols = model.feature_names_in_
    df = df.reindex(columns=model_cols, fill_value=0)

    # Lakukan prediksi
    prediction = model.predict(df)
    prediction_proba = model.predict_proba(df)

    return prediction[0], prediction_proba

# --- ANTARMUKA PENGGUNA (UI) ---
st.title("✈️ Prediksi Kepuasan Penumpang Pesawat")
st.write(
    "Aplikasi ini memprediksi apakah seorang penumpang akan puas atau tidak "
    "berdasarkan berbagai parameter layanan. Silakan isi form di bawah ini."
)

# Buat form input
with st.form("prediction_form"):
    st.header("Informasi Penumpang dan Penerbangan")

    # Buat layout kolom
    col1, col2 = st.columns(2)

    with col1:
        gender = st.selectbox("Jenis Kelamin", ["Female", "Male"])
        customer_type = st.selectbox("Tipe Pelanggan", ["Loyal Customer", "disloyal Customer"])
        age = st.slider("Usia", 1, 100, 35)
        type_of_travel = st.selectbox("Tipe Perjalanan", ["Business travel", "Personal Travel"])
        travel_class = st.selectbox("Kelas Penerbangan", ["Business", "Eco", "Eco Plus"])

    with col2:
        flight_distance = st.number_input("Jarak Penerbangan (km)", min_value=10, max_value=10000, value=1000)
        departure_delay = st.number_input("Keterlambatan Keberangkatan (menit)", min_value=0, max_value=1000, value=0)
        arrival_delay = st.number_input("Keterlambatan Kedatangan (menit)", min_value=0, max_value=1000, value=0)

    st.header("Rating Layanan (1-5)")
    
    # Layout 3 kolom untuk rating
    r_col1, r_col2, r_col3 = st.columns(3)
    
    with r_col1:
        inflight_wifi_service = st.slider("Layanan Wifi", 1, 5, 3)
        departure_arrival_time_convenient = st.slider("Kenyamanan Waktu", 1, 5, 3)
        ease_of_online_booking = st.slider("Kemudahan Booking Online", 1, 5, 3)
        gate_location = st.slider("Lokasi Gate", 1, 5, 3)
        
    with r_col2:
        food_and_drink = st.slider("Makanan & Minuman", 1, 5, 3)
        online_boarding = st.slider("Online Boarding", 1, 5, 3)
        seat_comfort = st.slider("Kenyamanan Kursi", 1, 5, 3)
        inflight_entertainment = st.slider("Hiburan di Pesawat", 1, 5, 3)
        
    with r_col3:
        onboard_service = st.slider("Layanan di Pesawat", 1, 5, 3)
        leg_room_service = st.slider("Ruang Kaki", 1, 5, 3)
        baggage_handling = st.slider("Penanganan Bagasi", 1, 5, 3)
        checkin_service = st.slider("Layanan Check-in", 1, 5, 3)
        inflight_service = st.slider("Layanan Penerbangan", 1, 5, 3)
        cleanliness = st.slider("Kebersihan", 1, 5, 3)


    # Tombol submit
    submitted = st.form_submit_button("Prediksi Kepuasan")

# --- HASIL PREDIKSI ---
if submitted:
    # Kumpulkan data dari form ke dalam dictionary
    input_data = {
        'Gender': gender, 
        'Customer Type': customer_type, 
        'Age': age, 
        'Type of Travel': type_of_travel, 
        'Class': travel_class, 
        'Flight Distance': flight_distance, 
        'Inflight wifi service': inflight_wifi_service,
        'Departure/Arrival time convenient': departure_arrival_time_convenient,
        'Ease of Online booking': ease_of_online_booking, 
        'Gate location': gate_location,
        'Food and drink': food_and_drink, 
        'Online boarding': online_boarding,
        'Seat comfort': seat_comfort, 
        'Inflight entertainment': inflight_entertainment,
        'On-board service': onboard_service, 
        'Leg room service': leg_room_service,
        'Baggage handling': baggage_handling, 
        'Checkin service': checkin_service,
        'Inflight service': inflight_service, 
        'Cleanliness': cleanliness,
        'Departure Delay in Minutes': departure_delay, 
        'Arrival Delay in Minutes': arrival_delay
    }
    
    # Panggil fungsi prediksi
    result_numeric, proba = predict(input_data)
    
    # --- Ubah hasil numerik menjadi label teks ---
    predicted_label = label_encoder.inverse_transform([result_numeric])[0]
    
    st.subheader("Hasil Prediksi")
    
    # --- Ambil probabilitas menggunakan nama kelas dari encoder ---
    class_names = label_encoder.classes_
    class_probabilities = dict(zip(class_names, proba[0]))
    
    satisfaction_proba = class_probabilities.get('satisfied', 0.0)
    neutral_proba = class_probabilities.get('neutral or dissatisfied', 0.0)
    
    # --- Gunakan label teks untuk logika if/else ---
    if predicted_label == 'satisfied':
        st.success(f"**Puas** (Tingkat keyakinan: {satisfaction_proba:.2%})")
        st.info("Terima kasih atas umpan balik positif Anda!")
    else: # 'neutral or dissatisfied'
        st.warning(f"**Netral atau Tidak Puas** (Tingkat keyakinan: {neutral_proba:.2%})")
        st.error("Kami mohon maaf atas ketidaknyamanan yang Anda alami.")

    st.write("Probabilitas detail:")
    st.write(f"- Puas: `{satisfaction_proba:.2%}`")
    st.write(f"- Netral/Tidak Puas: `{neutral_proba:.2%}`")