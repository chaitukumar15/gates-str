import streamlit as st
import requests
from google import genai

# ---------------- CONFIG ----------------

OPENWEATHER_API_KEY = "bf89bc2cde67abeceea98d4c23a10716"


# Initialize Gemini Client
client = genai.Client(api_key="AIzaSyBxDiCcFfvEBgnOb3ekb-Y5ujqEaRKJC4o")

# ---------------- UI ----------------

st.set_page_config(page_title="Alexa Weather Assistant", page_icon="🌤️")

st.title("🌤️ Alexa - Your Weather Assistant")
st.write("Get smart suggestions based on live weather data!")

cityname = st.text_input("Enter City Name")

if st.button("Get Weather Suggestions"):

    if cityname == "":
        st.warning("Please enter a city name")
    else:
        # ---------------- WEATHER API CALL ----------------

        api_url = f"https://api.openweathermap.org/data/2.5/weather?q={cityname}&appid={OPENWEATHER_API_KEY}&units=metric"

        response = requests.get(api_url)

        if response.status_code == 200:

            data_res_json = response.json()

            # Show basic weather info
            st.subheader("🌡️ Current Weather")
            st.write(f"Temperature: {data_res_json['main']['temp']} °C")
            st.write(f"Humidity: {data_res_json['main']['humidity']} %")
            st.write(f"Condition: {data_res_json['weather'][0]['description']}")

            # ---------------- GEMINI CALL ----------------
            with st.spinner("loading"):
                llm_response = client.models.generate_content(
                model="gemini-2.5-flash",
                contents=f"""
                Act as a weather assistant and your name is Alexa.
                Use this weather data: {data_res_json}

                Give suggestions in this format:

                City Name:
                Food:
                Clothing:
                Activity:
                Medication (if needed):
                
                Keep tone friendly and casual.
                """
            )

            st.subheader("🤖 Alexa Says:")
           
            st.success(llm_response.text)

        else:
            st.error("City not found. Please check spelling.")