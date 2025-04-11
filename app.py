from flask import Flask, request, jsonify
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

app = Flask(__name__)

# Utility to analyze nutrition gaps
def analyze_nutrition(data):
    gaps = []

    if data.get("greens") != "Daily":
        gaps.append("Low intake of green leafy vegetables (low iron, folate)")

    if data.get("fruits") != "Daily":
        gaps.append("Low fruit intake (low vitamin C, fiber)")

    if data.get("milk") == "Never":
        gaps.append("No dairy intake (low calcium and vitamin D)")

    if data.get("pulses") != "Daily":
        gaps.append("Low protein intake (pulses/dals)")

    if data.get("ifa_tablets") == "No":
        gaps.append("IFA tablets not taken (risk of iron deficiency)")

    if data.get("water_intake") == "<4":
        gaps.append("Low water intake (risk of dehydration)")

    if data.get("junk_food") == "Frequent":
        gaps.append("High junk food consumption (unhealthy fats)")

    if data.get("cost_constraints"):
        gaps.append("Missing nutrients due to affordability: " + ", ".join(data["cost_constraints"]))

    return gaps

# Create prompt for Gemini
def create_gemini_prompt(data, gaps):
    prompt = f"""
A pregnant woman from {data.get("region")} has shared her dietary information:

Meals per day: {data.get("meals_per_day")}
Green leafy vegetables: {data.get("greens")}
Fruits: {data.get("fruits")}
Milk/Dairy: {data.get("milk")}
Pulses/Dals: {data.get("pulses")}
Non-Veg: {data.get("non_veg")}
Packaged/Fried Food: {data.get("junk_food")}
IFA Tablets Taken: {data.get("ifa_tablets")}
Oil Usage: {data.get("oil_usage")}
Water Intake: {data.get("water_intake")}
Foods not consumed due to cost: {', '.join(data.get("cost_constraints", []))}

Detected Gaps:
- {chr(10).join(gaps)}

👉 Based on this, suggest a **simple, affordable, and local** daily diet plan using ingredients available in {data.get("region")}. The woman may be from a rural background, so use regional foods and simple language. Make sure the diet covers iron, folate, calcium, protein, and hydration.
"""
    return prompt

# Gemini call
def get_diet_from_gemini(prompt):
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(prompt)
    return response.text

# Main route
@app.route("/generate_diet", methods=["POST"])
def generate_diet():
    data = request.json
    gaps = analyze_nutrition(data)
    prompt = create_gemini_prompt(data, gaps)

    try:
        diet_plan = get_diet_from_gemini(prompt)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

    return jsonify({
        "diet_plan": diet_plan,
        "gaps_detected": gaps
    })

# Render deployment config
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
