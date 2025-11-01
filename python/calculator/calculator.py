from flask import Flask, render_template, request

# Initialize the Flask application
app = Flask(__name__)

# Define the options for the dropdown menu as a list of tuples
# Each tuple contains the display text and its corresponding value
operation_options = [
    ('Add', '1'),
    ('Subtract', '2'),
    ('Multiply', '3'),
    ('Divide', '4'),
    ('Floor Division', '5'),
    ('Reminder', '6')
]

# Define the route for the main page
@app.route('/', methods=['GET', 'POST'])
def home():
    result = None
    error = None
    # This block runs when the user submits the form
    if request.method == 'POST':
        try:
            num1 = float(request.form['num1'])
            num2 = float(request.form['num2'])
            operation = request.form['operation']

            if operation == '1':
                result = f"The sum is: {num1 + num2}"
            elif operation == '2':
                result = f"The difference is: {num1 - num2}"
            elif operation == '3':
                result = f"The product is: {num1 * num2}"
            elif operation == '4':
                if num2 != 0:
                    result = f"The division is: {num1 / num2}"
                else:
                    error = "Cannot divide by zero."
            elif operation == '5':
                if num2 != 0:
                    result = f"The floor division is: {num1 // num2}"
                else:
                    error = "Cannot divide by zero."
            elif operation == '6':
                if num2 != 0:
                    result = f"The reminder is: {num1 % num2}"
                else:
                    error = "Cannot divide by zero."
        except ValueError:
            error = "Invalid input. Please enter valid numbers."

    # Render the HTML page and pass the options and result to it
    return render_template('index.html', options=operation_options, result=result, error=error)

# This allows the script to be run directly
if __name__ == '__main__':
    app.run(debug=True)
