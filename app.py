# ============================
# AI/Smart Unit Converter - Enhanced Version
# ============================

import streamlit as st

# Page configuration
st.set_page_config(
    page_title="Smart Unit Converter",
    page_icon="🧮",
    layout="centered"
)

# Custom CSS for enhanced styling
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
        box-shadow: 0 8px 20px rgba(2,6,23,0.6);
    }
    .category-badge {
        background: linear-gradient(90deg, #60a5fa, #3b82f6);
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 0.8em;
        font-weight: bold;
    }
    .header-container {
        text-align: center;
        padding: 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Enhanced unit categories & units
units = {
    "Length": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", 
               "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
    "Weight": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lb)", "Ounce (oz)"],
    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"],
    "Volume": ["Liter (L)", "Milliliter (mL)", "Gallon (gal)", "Quart (qt)", "Pint (pt)", "Cup (cup)"],
    "Area": ["Square Meter (m²)", "Square Kilometer (km²)", "Square Foot (ft²)", 
             "Square Inch (in²)", "Acre (ac)", "Hectare (ha)"],
    "Time": ["Second (s)", "Minute (min)", "Hour (hr)", "Day (day)", "Week (week)", "Month (month)", "Year (year)"],
    "Digital Storage": ["Byte (B)", "Kilobyte (KB)", "Megabyte (MB)", "Gigabyte (GB)", "Terabyte (TB)"]
}

# Enhanced conversion functions
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
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    # Weight conversions
    elif category == "Weight":
        factors = {
            "Kilogram (kg)": 1, "Gram (g)": 0.001, "Milligram (mg)": 0.000001,
            "Pound (lb)": 0.453592, "Ounce (oz)": 0.0283495
        }
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

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
        
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    # Volume conversions
    elif category == "Volume":
        factors = {
            "Liter (L)": 1,
            "Milliliter (mL)": 0.001,
            "Gallon (gal)": 3.78541,
            "Quart (qt)": 0.946353,
            "Pint (pt)": 0.473176,
            "Cup (cup)": 0.24
        }
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    # Area conversions
    elif category == "Area":
        factors = {
            "Square Meter (m²)": 1,
            "Square Kilometer (km²)": 1000000,
            "Square Foot (ft²)": 0.092903,
            "Square Inch (in²)": 0.00064516,
            "Acre (ac)": 4046.86,
            "Hectare (ha)": 10000
        }
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    # Time conversions
    elif category == "Time":
        factors = {
            "Second (s)": 1,
            "Minute (min)": 60,
            "Hour (hr)": 3600,
            "Day (day)": 86400,
            "Week (week)": 604800,
            "Month (month)": 2592000,  # 30 days
            "Year (year)": 31536000   # 365 days
        }
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    # Digital Storage conversions
    elif category == "Digital Storage":
        factors = {
            "Byte (B)": 1,
            "Kilobyte (KB)": 1024,
            "Megabyte (MB)": 1048576,
            "Gigabyte (GB)": 1073741824,
            "Terabyte (TB)": 1099511627776
        }
        v_base = v * factors[from_unit]
        result = v_base / factors[to_unit]
        return f"**{v} {from_unit} = {round(result, 6)} {to_unit}**"

    return "⚠️ Conversion not supported."

# Main app interface
def main():
    # Header with badge
    st.markdown("""
    <div class="header-container">
        <h1 style='color:#e6eef8; margin-bottom:10px;'>🧮 Smart Unit Converter</h1>
        <div class="category-badge">7 Categories • 40+ Units</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Input section
    col1, col2 = st.columns([1, 1])
    
    with col1:
        value = st.number_input("**Value**", value=1.0, step=1.0, format="%.6f")
        category = st.selectbox("**Category**", list(units.keys()))
    
    with col2:
        from_unit = st.selectbox("**From Unit**", units[category])
        to_unit = st.selectbox("**To Unit**", units[category])
    
    # Convert button
    if st.button("**Convert 🔄**"):
        result = convert_units(value, category, from_unit, to_unit)
        st.markdown(f"""
        <div class="result-box">
            <h3 style='margin:0; color:#60a5fa;'>📊 Conversion Result:</h3>
            <div style='font-size:1.3em; margin:15px 0; text-align:center;'>{result}</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Categories info
    st.markdown("---")
    st.markdown("### 📚 Available Categories")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**📏 Length**\n- 8 units")
    with col2:
        st.markdown("**⚖️ Weight**\n- 5 units")
    with col3:
        st.markdown("**🌡️ Temperature**\n- 3 units")
    with col4:
        st.markdown("**🧪 Volume**\n- 6 units")
    
    col5, col6, col7 = st.columns(3)
    with col5:
        st.markdown("**📐 Area**\n- 6 units")
    with col6:
        st.markdown("**⏰ Time**\n- 7 units")
    with col7:
        st.markdown("**💾 Digital Storage**\n- 5 units")

if __name__ == "__main__":
    main()
