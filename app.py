
import streamlit as st
from predict import predict_irrigation
from chatboat import get_chatbot_response

st.set_page_config(
    page_title="Smart Irrigation System",
    layout="wide"
)

st.title("Smart Irrigation System")
st.write(
    "Predict irrigation requirements and get smart farming guidance."
)

# ---------------- Irrigation Prediction ----------------

st.header("Irrigation Requirement Prediction")

with st.form("irrigation_form"):
    col1, col2 = st.columns(2)

    with col1:
        soil_ph = st.number_input(
            "Soil pH", min_value=0.0, max_value=14.0, value=6.5
        )
        soil_moisture = st.number_input(
            "Soil Moisture", min_value=0.0, value=30.0
        )
        organic_carbon = st.number_input(
            "Organic Carbon", min_value=0.0, value=1.5
        )
        conductivity = st.number_input(
            "Electrical Conductivity", min_value=0.0, value=0.5
        )
        temperature = st.number_input(
            "Temperature (°C)", value=28.0
        )
        humidity = st.number_input(
            "Humidity (%)", min_value=0.0, max_value=100.0, value=60.0
        )

    with col2:
        rainfall = st.number_input(
            "Rainfall (mm)", min_value=0.0, value=5.0
        )
        sunlight = st.number_input(
            "Sunlight Hours", min_value=0.0, value=7.0
        )
        wind_speed = st.number_input(
            "Wind Speed (km/h)", min_value=0.0, value=10.0
        )
        field_area = st.number_input(
            "Field Area (hectares)", min_value=0.0, value=1.0
        )
        previous_irrigation = st.number_input(
            "Previous Irrigation (mm)", min_value=0.0, value=10.0
        )

    water_source = st.selectbox(
        "Water Source", ["River","Reservoir","Rainwater","Groundwater"]
    )
    mulching = st.selectbox("Mulching Used", ["Yes", "No"])
    region = st.selectbox("Region", ["south", "West", "East","Central","North"])
    soil_type = st.selectbox(
        "Soil Type", ["Clay", "Loamy", "Sandy", "Silt"]
    )
    crop_type = st.selectbox(
        "Crop Type", ["Wheat", "Rice", "Maize", "Cotton", "Sugarcane","Potato"]
    )
    growth_stage = st.selectbox(
        "Crop Growth Stage",
        ["Sowing", "Vegetative", "Flowering", "Harvest"]
    )
    season = st.selectbox(
        "Season", ["Rabi", "Kharif", "Zaid"]
    )
    irrigation_type = st.selectbox(
        "Irrigation Type", ["Drip", "Sprinkler", "Rainfed", "Canal"]
    )

    predict_button = st.form_submit_button("Predict Irrigation Need")

if predict_button:
    input_data = {
        "Soil_pH": soil_ph,
        "Soil_Moisture": soil_moisture,
        "Organic_Carbon": organic_carbon,
        "Electrical_Conductivity": conductivity,
        "Temperature_C": temperature,
        "Humidity": humidity,
        "Rainfall_mm": rainfall,
        "Sunlight_Hours": sunlight,
        "Wind_Speed_kmh": wind_speed,
        "Field_Area_hectare": field_area,
        "Previous_Irrigation_mm": previous_irrigation,
        "Water_Source": water_source,
        "Mulching_Used": mulching,
        "Region": region,
        "Soil_Type": soil_type,
        "Crop_Type": crop_type,
        "Crop_Growth_Stage": growth_stage,
        "Season": season,
        "Irrigation_Type": irrigation_type,
    }

    try:
        result = predict_irrigation(input_data)
        st.session_state["last_prediction"] = result

        st.success(f"Predicted Irrigation Need: **{result}**")

    except Exception as error:
        st.error(f"Prediction failed: {error}")


# ---------------- Ollama Chatbot ----------------

st.divider()
st.header("Smart Irrigation Chatbot")
st.caption("Powered by Ollama and Llama 3.2 (1B)")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display previous conversation
for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_question = st.chat_input(
    "Ask about irrigation, crops, soil, or water conservation..."
)

if user_question:
    # Display the user's message
    st.session_state.chat_history.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.markdown(user_question)

    # Prepare conversation history for Ollama
    history = [
        {"role": message["role"], "content": message["content"]}
        for message in st.session_state.chat_history[:-1]
        if message["role"] in ("user", "assistant")
    ]

    # Generate the chatbot response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                answer = get_chatbot_response(
                    user_question,
                    history=history
                )
                st.markdown(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as error:
                st.error(
                    "Could not connect to Ollama. "
                    "Make sure Ollama is running and "
                    "llama3.2:1b is installed."
                )
                st.caption(f"Error details: {error}")
