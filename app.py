from flask import Flask, request, jsonify, render_template
import openai
import os

app = Flask(__name__)

# Ensure you have your OpenAI API key set as an environment variable
openai.api_key =("YOUR API KEY")

def generate_with_openai(prompt):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",  # Adjust with the model you prefer
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ]
    )
    return response.choices[0].message['content'].strip()

def get_workout_plan(workout_requirement):
    prompt = f"Provide a {workout_requirement} workout plan."
    return generate_with_openai(prompt)

# Define the get_meal_plan function
def get_meal_plan(diet_type, goal):
    prompt = f"Provide a meal plan for someone who follows a {diet_type} diet and is looking to {goal} weight."
    return generate_with_openai(prompt)

@app.route('/')
def index():
    return render_template('2.html')  # Make sure you have this HTML file prepared

@app.route('/get_workout_plan', methods=['POST'])
def workout_plan():
    workout_requirement = request.json['workout_requirement']
    plan = get_workout_plan(workout_requirement)
    return jsonify(plan=plan)

@app.route('/get_meal_plan', methods=['POST'])
def meal_plan():
    diet_type = request.json['diet_type']
    goal = request.json['goal']
    plan = get_meal_plan(diet_type, goal)
    return jsonify(plan=plan)

# Add the missing BMI calculation function here if it's part of your application
def calculate_bmi(height, weight):
    bmi = weight / (height ** 2)
    return bmi

@app.route('/calculate_bmi', methods=['POST'])
def bmi():
    height = float(request.json['height'])
    weight = float(request.json['weight'])
    bmi_result = calculate_bmi(height, weight)
    return jsonify(bmi=f"{bmi_result:.2f}")

if __name__ == '__main__':
    app.run(debug=True)
