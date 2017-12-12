# Import section
import os
from flask import Flask,render_template,abort,jsonify

# Initializing app
app = Flask(__name__)
RESULTS_DIR = "results";

@app.route('/')
def hello_world():
    
    # Listing all folder inside "results" folder
    return render_template("index.html",dirs=os.listdir(RESULTS_DIR))
    
@app.route('/<string:dir>')
def display_graph(dir):

    # Creating path
    path = "".join([RESULTS_DIR,"/",dir,"/","csv"])

    # Listing all files in the directory
    files = [f for f in os.listdir(path) if os.path.isfile(os.path.join(path, f))]
    
    # Sending response
    return render_template("results.html",files=files)
    
@app.route('/<string:dir>/<string:fileName>')
def return_data(dir,fileName):

    # Creating path
    path = os.path.join(RESULTS_DIR,dir,"csv",fileName)
    
    # Additinal imports
    import csv,json

    # Creating path
    if not os.path.isfile(path):
        abort(404)
        
    # Reading the file contents
    with open(path) as f:
        csv_content = f.read()
        
    # Getting the fieldnames
    lines = csv_content.splitlines()
    fieldNames = lines[0].split(",")
    fieldNames[0] = "labels"
    
    # Creating data structure
    data = {}
    for name in fieldNames:
        data[name] = []
        
    # Creating a new array without the first line
    lines = csv_content.splitlines()[1:]
    
    # Parsing each line
    for line in lines:
            
        # Parsing the line
        array = line.split(",")
        index = 0
        
        for value in array:
            data[fieldNames[index]].append(value)
            index = index + 1
    return jsonify(data)


# Running the app
if __name__ == '__main__':
    app.run(host="0.0.0.0",debug=True)