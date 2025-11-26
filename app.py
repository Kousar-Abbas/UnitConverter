# ============================
# AI/Smart Unit Converter - Streamlit Version
# ============================

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Smart Unit Converter",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for styling
st.markdown("""
<style>
    .main {
        background: linear-gradient(135deg, #0f172a 0%, #0b1220 30%, #1f2937 100%);
        color: white;
    }
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3em;
        background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02));
        border: 1px solid rgba(255,255,255,0.06);
        color: #e6eef8;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 16px rgba(0,0,0,0.3);
    }
    .result-box {
        background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01));
        border-radius: 12px;
        padding: 20px;
        color: #dbeafe;
        font-weight: 600;
        border: 1px solid rgba(255,255,255,0.04);
        margin-top: 20px;
    }
</style>
""", unsafe_allow_html=True)

# Unit categories & units
units = {
    "Length": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", 
               "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
    "Weight": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lb)", "Ounce (oz)"],
    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
}

# Conversion functions
def convert_units(value, category, from_unit, to_unit):
    try:
        v = float(value)
    except:
        return "⚠️ Enter a valid numeric value."

    # Length conversions
    if category == "Length":
        factors = {
            "Meter (m)": 1, "Kilometer (km)": 1000, "Centimeter (cm)": 0.01,
            "Millimeter (mm)": 0.001, "Mile (mi)": 1609.34, "Yard (yd)": 0.9144,
            "Foot (ft)": 0.3048, "Inch (in)": 0.0254
        }
        v_meters = v * factors[from_unit]
        result = v_meters / factors[to_unit]
        return f"{v} {from_unit} = {round(result, 6)} {to_unit}"

    # Weight conversions
    elif category == "Weight":
        factors = {
            "Kilogram (kg)": 1, "Gram (g)": 0.001, "Milligram (mg)": 0.000001,
            "Pound (lb)": 0.453592, "Ounce (oz)": 0.0283495
        }
        v_kg = v * factors[from_unit]
        result = v_kg / factors[to_unit]
        return f"{v} {from_unit} = {round(result, 6)} {to_unit}"

    # Temperature conversions
    elif category == "Temperature":
        # Convert from_unit -> Celsius -> to_unit
        if from_unit == "Celsius (°C)":
            c = v
        elif from_unit == "Fahrenheit (°F)":
            c = (v - 32) * 5 / 9
        elif from_unit == "Kelvin (K)":
            c = v - 273.15
        
        # Celsius -> target
        if to_unit == "Celsius (°C)":
            result = c
        elif to_unit == "Fahrenheit (°F)":
            result = c * 9 / 5 + 32
        elif to_unit == "Kelvin (K)":
            result = c + 273.15
        
        return f"{v} {from_unit} = {round(result, 6)} {to_unit}"

    return "⚠️ Conversion not supported."

# Main app interface
def main():
    st.markdown("<h1 style='text-align:center;color:#e6eef8;'>🧮 Smart Unit Converter</h1>", 
                unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        value = st.number_input("Value", value=1.0, step=1.0)
        category = st.selectbox("Category", list(units.keys()))
    
    with col2:
        from_unit = st.selectbox("From Unit", units[category])
        to_unit = st.selectbox("To Unit", units[category])
    
    # Convert button
    if st.button("Convert 🔄"):
        result = convert_units(value, category, from_unit, to_unit)
        st.markdown(f"""
        <div class="result-box">
            <h3 style='margin:0; color:#60a5fa;'>Conversion Result:</h3>
            <p style='font-size:1.2em; margin:10px 0;'>{result}</p>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
