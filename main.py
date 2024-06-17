from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Dict

app = FastAPI()

class UserInfo(BaseModel):
    weight: float  # in kg
    height: float  # in cm
    age: int
    gender: str  # 'male' or 'female'
    activity_level: float  # activity factor

@app.get("/activity_levels/")
async def get_activity_levels() -> List[Dict[str, str]]:
    activity_levels = [
        {"level": "1.2", "description": "Sedentary (little or no exercise)"},
        {"level": "1.375", "description": "Lightly active (light exercise/sports 1-3 days/week)"},
        {"level": "1.55", "description": "Moderately active (moderate exercise/sports 3-5 days/week)"},
        {"level": "1.725", "description": "Very active (hard exercise/sports 6-7 days a week)"},
        {"level": "1.9", "description": "Super active (very hard exercise/sports & physical job or 2x training)"}
    ]
    return activity_levels

@app.post("/calculate_macros/")
async def calculate_macros(user_info: UserInfo):
    weight = user_info.weight
    height = user_info.height
    age = user_info.age
    gender = user_info.gender.lower()
    activity_level = user_info.activity_level

    # Calculate BMR using Harris-Benedict equation
    if gender == 'male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        return {"error": "Invalid gender. Please use 'male' or 'female'."}

    # Calculate total daily calorie needs
    total_calories = bmr * activity_level

    # Calculate protein requirements
    protein_grams = weight * 2
    protein_calories = protein_grams * 4

    # Calculate fat requirements
    fat_calories = total_calories * 0.25
    fat_grams = fat_calories / 9

    # Calculate remaining calories for carbs
    remaining_calories = total_calories - (protein_calories + fat_calories)
    carb_grams = remaining_calories / 4

    return {
        "bmr": bmr,
        "total_calories": total_calories,
        "protein_grams": protein_grams,
        "protein_calories": protein_calories,
        "fat_grams": fat_grams,
        "fat_calories": fat_calories,
        "carb_grams": carb_grams,
        "carb_calories": remaining_calories
    }

@app.post("/calculate_bmi/")
async def calculate_bmi(user_info: UserInfo):
    weight = user_info.weight
    height = user_info.height
    bmi = weight / ((height / 100) ** 2)
    return {
        "bmi": bmi
    }
