import os
import json
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load optimization rules from the JSON file
with open('rules.json', 'r') as f:
    optimization_rules = json.load(f)["rules"]

def optimize_prompt(prompt):
    prompt = prompt.strip()  # Trim leading and trailing spaces

    # Flag to track if essay-related responses should be applied
    is_essay = False
    is_step_by_step = False

    # Check if the prompt is asking for an essay or a step-by-step guide
    for rule in optimization_rules:
        if "keywords" in rule:
            for keyword in rule["keywords"]:
                if keyword.lower() in prompt.lower():
                    # Set flags based on rule types
                    if "essay" in rule["type"]:
                        is_essay = True
                    elif "step_by_step" in rule["type"]:
                        is_step_by_step = True
                    break
        if is_essay or is_step_by_step:
            break

    # Apply specific rules based on the type of prompt
    for rule in optimization_rules:
        if "keywords" in rule:
            for keyword in rule["keywords"]:
                if keyword.lower() in prompt.lower():
                    # Prevent essay-specific responses from being applied to non-essay prompts
                    if "essay" in rule["type"] and not is_essay:
                        continue
                    if "step_by_step" in rule["type"] and not is_step_by_step:
                        continue
                    prompt += " " + rule["response"]
                    break

    return prompt

@app.route('/optimize', methods=['POST'])
def optimize():
    data = request.get_json()
    prompt = data.get('prompt', '')
    optimized_prompt = optimize_prompt(prompt)
    return jsonify({"optimizedPrompt": optimized_prompt})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))

