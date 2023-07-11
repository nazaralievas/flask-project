from flask import Flask, render_template
app = Flask(__name__)

@app.route('/')
def homepage():
    products = {'IPhone': 1100,
                'Samsung': 650,
                'Xiaomi': 450}
    return render_template('homepage.html', products=products)

@app.route('/about')
def about():
    return render_template('about.html')


if __name__ == "__main__":
    app.run(debug=True)


# pip install flask-sqlalchemy
