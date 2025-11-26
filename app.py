# ============================
# Hugging Face-ready Unit Converter
# ============================

import os
import gradio as gr
import requests

# ----------------------------
# Groq API key (optional, for AI tips)
# ----------------------------
GROQ_API_KEY = os.environ.get("GROQ_API_KEY")
GROQ_CHAT_COMPLETIONS_URL = "https://api.groq.com/openai/v1/chat/completions"

# ----------------------------
# Unit categories & units
# ----------------------------
units = {
    "Length": ["Meter (m)", "Kilometer (km)", "Centimeter (cm)", "Millimeter (mm)", "Mile (mi)", "Yard (yd)", "Foot (ft)", "Inch (in)"],
    "Weight": ["Kilogram (kg)", "Gram (g)", "Milligram (mg)", "Pound (lb)", "Ounce (oz)"],
    "Temperature": ["Celsius (°C)", "Fahrenheit (°F)", "Kelvin (K)"]
}

# ----------------------------
# Conversion logic
# ----------------------------
def convert_units(value, category, from_unit, to_unit):
    try:
        v = float(value)
    except:
        return "⚠️ Enter a valid numeric value."
    
    # Length
    if category == "Length":
        factors = {"Meter (m)":1, "Kilometer (km)":1000, "Centimeter (cm)":0.01,
                   "Millimeter (mm)":0.001, "Mile (mi)":1609.34, "Yard (yd)":0.9144,
                   "Foot (ft)":0.3048, "Inch (in)":0.0254}
        v_meters = v * factors[from_unit]
        result = v_meters / factors[to_unit]
        return f"{v} {from_unit} = {round(result,6)} {to_unit}"

    # Weight
    elif category == "Weight":
        factors = {"Kilogram (kg)":1, "Gram (g)":0.001, "Milligram (mg)":0.000001,
                   "Pound (lb)":0.453592, "Ounce (oz)":0.0283495}
        v_kg = v * factors[from_unit]
        result = v_kg / factors[to_unit]
        return f"{v} {from_unit} = {round(result,6)} {to_unit}"

    # Temperature
    elif category == "Temperature":
        if from_unit == "Celsius (°C)":
            c = v
        elif from_unit == "Fahrenheit (°F)":
            c = (v-32)*5/9
        elif from_unit == "Kelvin (K)":
            c = v-273.15

        if to_unit == "Celsius (°C)":
            result = c
        elif to_unit == "Fahrenheit (°F)":
            result = c*9/5+32
        elif to_unit == "Kelvin (K)":
            result = c+273.15

        return f"{v} {from_unit} = {round(result,6)} {to_unit}"

    return "⚠️ Conversion not supported."

# ----------------------------
# Optional AI Tips via Groq
# ----------------------------
def generate_ai_tip(category, from_unit, to_unit, value, result):
    if not GROQ_API_KEY:
        return "⚡ AI tip unavailable (set GROQ_API_KEY in Secrets)."
    try:
        system_prompt = "You are a smart assistant giving concise, helpful tips about unit conversions."
        user_prompt = f"Conversion: {value} {from_unit} = {result} {to_unit}. Give a smart tip or interesting fact in 1-2 sentences."
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"model":"gpt-3.5-turbo",
                   "messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_prompt}],
                   "temperature":0.3,"max_tokens":80}
        resp = requests.post(GROQ_CHAT_COMPLETIONS_URL, headers=headers, json=payload, timeout=15)
        if resp.status_code != 200:
            return "⚡ AI tip error."
        j = resp.json()
        if "choices" in j and len(j["choices"])>0:
            return j["choices"][0].get("message",{}).get("content","")
        return "⚡ AI tip error."
    except:
        return "⚡ AI tip error."

# ----------------------------
# Wrapper for Gradio
# ----------------------------
def convert_and_tip(value, category, from_unit, to_unit):
    result_text = convert_units(value, category, from_unit, to_unit)
    tip_text = generate_ai_tip(category, from_unit, to_unit, value, result_text)
    return result_text, tip_text

# ----------------------------
# Gradio UI
# ----------------------------
css_style = """
body, .gradio-container {background: linear-gradient(135deg, #0f172a 0%, #0b1220 30%, #1f2937 100%);}
.gr-button {transition: transform 0.2s, box-shadow 0.2s; border-radius:12px; box-shadow:6px 8px 0 rgba(0,0,0,0.38); color:#e6eef8 !important; background: linear-gradient(90deg, rgba(255,255,255,0.06), rgba(255,255,255,0.02)); border:1px solid rgba(255,255,255,0.06);}
.gr-button:hover{transform:translateY(-3px) scale(1.01); box-shadow:12px 16px 0 rgba(0,0,0,0.42);}
.gr-button:active{transform:translateY(0px) scale(0.995); box-shadow:4px 6px 0 rgba(0,0,0,0.5);}
.result-box {background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); border-radius:12px; padding:12px; color:#dbeafe; font-weight:600; border:1px solid rgba(255,255,255,0.04); box-shadow:0 8px 20px rgba(2,6,23,0.6);}
.result-ai {background: linear-gradient(180deg, rgba(255,255,255,0.02), rgba(255,255,255,0.01)); padding:12px; border-radius:10px; color:#e6eef8; border:1px solid rgba(255,255,255,0.04); box-shadow:0 8px 20px rgba(2,6,23,0.6);}
"""

with gr.Blocks(css=css_style) as demo:
    gr.Markdown("<h2 style='text-align:center;color:#e6eef8;'>🧮 Smart Unit Converter</h2>")
    
    with gr.Row():
        with gr.Column(scale=1):
            value_input = gr.Number(value=1, label="Value")
            category = gr.Dropdown(list(units.keys()), value="Length", label="Category")
            from_unit = gr.Dropdown(units["Length"], value="Meter (m)", label="From Unit")
            to_unit = gr.Dropdown(units["Length"], value="Kilometer (km)", label="To Unit")
            convert_btn = gr.Button("Convert 🔄")
        with gr.Column(scale=2):
            result_md = gr.Markdown("", elem_classes="result-box")
            tip_md = gr.Markdown("", elem_classes="result-ai")
    
    # Update units dynamically when category changes
    def update_units(cat):
        return gr.update(choices=units[cat], value=units[cat][0]), gr.update(choices=units[cat], value=units[cat][1])
    category.change(update_units, category, [from_unit, to_unit])
    
    convert_btn.click(convert_and_tip, [value_input, category, from_unit, to_unit], [result_md, tip_md])

app = demo

if __name__ == "__main__":
    app.launch()
