from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI
app = FastAPI()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-1.5-pro-001")

# Input model
class DietInput(BaseModel):
    meals_per_day: str
    leafy_veggies: str
    fruits: str
    dairy: str
    pulses: str
    non_veg: str
    packaged_food: str
    iron_rich: str
    ifa_tablets: str
    staple_quantity: str
    oil_usage: str
    water_intake: str
    tea_coffee: str
    food_budget: str = None
    affordability_constraints: str = None
    state: str
    district: str

@app.post("/generate-monthly-diet")
async def generate_monthly_diet(data: DietInput):
    prompt = f"""
You are a healthcare assistant for a government maternity program. 

Generate a **simple weekly diet plan for a pregnant woman** from **{state}, {district}**, which is a **non-urban (rural) area** in India. The diet should use **locally available, low-cost foods** and be suitable for **low-income families**.

Input parameters:
- Meals/day: {meals_per_day}
- Green leafy vegetables: {leafy_veggies}
- Fruits: {fruits}
- Dairy: {dairy}
- Pulses: {pulses}
- Non-veg: {non_veg}
- Packaged/fried food: {packaged_food}
- Iron-rich food: {iron_rich}
- IFA tablets: {ifa_tablets}
- Staple quantity: {staple_quantity}
- Oil usage: {oil_usage}
- Water intake: {water_intake}
- Tea/Coffee: {tea_coffee}
- Budget: {food_budget}
- Food affordability issues: {affordability_constraints}
- Location: {district}, {state}

**Instructions:**
- Suggest a **4-week plan**, with one block per week (not daily breakdown).
- Meals per day can be summarized (e.g., Breakfast / Lunch / Dinner / Snack).
- Use simple ingredients common in rural India (e.g., dal, rice, roti, green leafy vegetables, chana, jaggery).
- Avoid expensive items like paneer, dry fruits, chicken, etc., **unless affordable**.
- If items like milk or fruits are not affordable (mentioned above), suggest substitutes or remove them.
- Include **1 tip per week** for improving iron/calcium intake or general pregnancy health.
- Keep the response **short and practical** for rural women (no lengthy explanations).
- Use simple Hindi-friendly terms (like sabzi, dal, roti) in English text.

Output should look like:
Week 1:
Breakfast – ...
Lunch – ...
Dinner – ...
Snack – ...
Tip – ...
"""


    response = model.generate_content(prompt)
    return {"monthly_diet_plan": response.text.strip()}
