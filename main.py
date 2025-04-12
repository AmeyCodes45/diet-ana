from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
import os

# Initialize FastAPI
app = FastAPI()

# Configure Gemini API
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-pro")

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
    You are a healthcare nutritionist preparing a simple monthly diet plan for a pregnant woman in rural India.

    ➤ Divide the response into 4 weeks. For each week, include:
    - Breakfast (typical options)
    - Lunch (typical options)
    - Dinner (typical options)
    - 1 healthy snack suggestion
    - 1 simple tip about fluids or iron

    ➤ Don't list all 7 days. Just give a weekly meal pattern that can be followed. Keep response short and easy to understand.

    --- User's Inputs ---
    Meals per day: {data.meals_per_day}
    Green leafy vegetables: {data.leafy_veggies}
    Fruits: {data.fruits}
    Dairy: {data.dairy}
    Pulses: {data.pulses}
    Non-veg: {data.non_veg}
    Packaged/fried food: {data.packaged_food}
    Iron-rich food consumed: {data.iron_rich}
    IFA tablets taken: {data.ifa_tablets}
    Staple quantity: {data.staple_quantity}
    Oil used daily: {data.oil_usage}
    Water per day: {data.water_intake}
    Tea/coffee intake: {data.tea_coffee}
    Monthly food budget: {data.food_budget or 'Not shared'}
    Skipped foods due to cost: {data.affordability_constraints or 'None'}
    Location: {data.district}, {data.state}

    ➤ Personalize based on local, affordable, nutritious, and practical rural Indian context.
    ➤ Response must be structured by **Week 1, Week 2, Week 3, Week 4** with only the meal types mentioned.
    ➤ Don’t use paragraphs. Avoid any lengthy text or nutritional theory.
    """

    response = model.generate_content(prompt)
    return {"monthly_diet_plan": response.text.strip()}
