import pandas as pd
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Load the Excel data into pandas DataFrame
options_df = pd.read_excel('options.xlsx', sheet_name='options')  # Adjust sheet name if necessary
images_df = pd.read_excel('images.xlsx', sheet_name='images')  # Adjust sheet name if necessary

# Clean column names to remove any extra spaces or special characters
images_df.columns = images_df.columns.str.strip()

@app.route('/')
def index():
    # Extract available options for the user
    options = {
        'material_finish': options_df[options_df['Option Type'] == 'Material & Finish']['Option Value'].tolist(),
        'width': options_df[options_df['Option Type'] == 'Width']['Option Value'].tolist(),
        'length': options_df[options_df['Option Type'] == 'Length']['Option Value'].tolist(),
        'insulation_bracket': options_df[options_df['Option Type'] == 'Insulation & Bracket']['Option Value'].tolist(),
        'conductor_size': options_df[options_df['Option Type'] == 'Conductor Size']['Option Value'].tolist(),
        'conductor_length_location': options_df[options_df['Option Type'] == 'Conductor Length & Location']['Option Value'].tolist(),
    }

    return render_template('index.html', options=options)

@app.route('/get_hole_patterns', methods=['POST'])
def get_hole_patterns():
    # Get the selected width from the user
    selected_width = request.form.get('width')

    # Filter hole patterns based on the selected width
    hole_images = {}
    for _, row in images_df.iterrows():
        # Split the Width1 column into a list
        widths = str(row['Width1']).split(',')
        if selected_width in widths:  # Check if the selected width is in the list
            hole_images[row['Hole Pattern']] = f"static/images/{row['Image File']}"

    # Return the filtered hole patterns as JSON
    return jsonify(hole_images)

@app.route('/generate_part_number', methods=['POST'])
def generate_part_number():
    # Get selected options from the user
    material_finish = request.form.get('material_finish')
    width = request.form.get('width')
    length = request.form.get('length')
    hole_pattern = request.form.get('hole_pattern')
    insulation_bracket = request.form.get('insulation_bracket')
    conductor_size = request.form.get('conductor_size')
    conductor_length_location = request.form.get('conductor_length_location')

    # Dynamically generate part number
    part_number = f"TB-{material_finish}-{width}-{length}-{hole_pattern}-{insulation_bracket}-{conductor_size}-{conductor_length_location}"

    # Fetch image URL based on hole pattern
    hole_image = f"static/images/pattern_{hole_pattern.zfill(2)}.jpg"

    return jsonify({
        'part_number': part_number,
        'hole_image': hole_image
    })

if __name__ == '__main__':
    app.run(debug=True)
