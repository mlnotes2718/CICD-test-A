from flask import Flask, jsonify, request, render_template_string

app = Flask(__name__)


HTML_PAGE = """
<!doctype html>
<html lang=\"en\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>BMI Calculator</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 420px; margin: 40px auto; }
    form { display: flex; flex-direction: column; gap: 10px; }
    input, button { padding: 10px; font-size: 16px; }
    #result { margin-top: 15px; font-weight: bold; }
  </style>
</head>
<body>
  <h1>BMI Calculator</h1>
  <form id=\"bmi-form\">
    <input id=\"weight\" type=\"number\" step=\"0.01\" placeholder=\"Weight (kg)\" required>
    <input id=\"height\" type=\"number\" step=\"0.01\" placeholder=\"Height (m)\" required>
    <button type=\"submit\">Calculate BMI</button>
  </form>
  <div id=\"result\"></div>

  <script>
    document.getElementById('bmi-form').addEventListener('submit', async function (e) {
      e.preventDefault();
      const weight = document.getElementById('weight').value;
      const height = document.getElementById('height').value;
      const response = await fetch('/api/bmi', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ weight_kg: parseFloat(weight), height_m: parseFloat(height) })
      });
      const data = await response.json();
      const result = document.getElementById('result');
      if (response.ok) {
        result.textContent = `BMI: ${data.bmi.toFixed(2)} (${data.category})`;
      } else {
        result.textContent = data.error || 'Invalid input';
      }
    });
  </script>
</body>
</html>
"""


def calculate_bmi(weight_kg: float, height_m: float) -> float:
    if height_m <= 0:
        raise ValueError("Height must be greater than zero")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than zero")
    return weight_kg / (height_m * height_m)


def bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    if bmi < 25:
        return "Normal weight"
    if bmi < 30:
        return "Overweight"
    return "Obesity"


@app.route("/", methods=["GET"])
def index():
    return render_template_string(HTML_PAGE)


@app.route("/api/bmi", methods=["POST"])
def bmi_api():
    payload = request.get_json(silent=True) or {}
    weight_kg = payload.get("weight_kg")
    height_m = payload.get("height_m")

    try:
        weight = float(weight_kg)
        height = float(height_m)
        bmi = calculate_bmi(weight, height)
    except (TypeError, ValueError):
        return jsonify({"error": "Please provide valid numeric values for weight_kg and height_m."}), 400

    return jsonify({"bmi": round(bmi, 2), "category": bmi_category(bmi)})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
