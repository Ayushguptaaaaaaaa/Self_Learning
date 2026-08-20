from flask import Flask, request, render_template

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def hello_world(): 
    if(request.method == "POST"):
        # Handle the form 
        with open("file.txt", "w") as f:
            f.write(f"The name is {request.form['name']} and email is {request.form['email']} ")
        return render_template("contact.html") 
        
    else:
        return render_template("contact.html")

app.run(debug=True)