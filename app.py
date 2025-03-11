from flask import Flask, render_template

app = Flask(__name__)

# Static project data (Modify as needed)
projects = [
    {
        "title": "Car Race Game",
        "description": "A simple web-based driving game created using JavaScript, HTML, CSS, and Flask. The player controls a car and avoids obstacles on the road.",
        "link": "https://bumblebee-race-game.onrender.com/"
    },
    {
        "title": "Portfolio Website",
        "description": "A personal portfolio website built with Flask, HTML, and CSS. It showcases projects, achievements, and contact details.",
        "link": "https://mahekthakur2245.onrender.com/"
    },
    {
        "title": "Case Study: Breast Cancer Detection Using Machine Learning",
        "description": "Breast cancer is one of the most common cancers worldwide, and early detection significantly improves survival rates. This case study focuses on leveraging machine learning (ML) techniques to build a predictive model that can classify breast cancer tumors as benign or malignant based on medical data.",
        "link": ""
    },
    {
        "title": "House Price Prediction using machine learning",
        "description": "Predicting house prices is a crucial task in real estate, as it helps buyers, sellers, and investors make informed decisions. This study focuses on building a machine learning model that predicts house prices based on various features such as location, size, number of bedrooms, and amenities.",
        "link": ""

    }
]

# Home Route
@app.route('/')
def home():
    github_url = "https://github.com/mahek2245"
    linkedin_url = "https://in.linkedin.com/in/mahek-thakur-095381324"
    return render_template('index.html', github_url=github_url, linkedin_url=linkedin_url)

# Projects Route
@app.route('/projects')
def projects():
    return render_template('projects.html', projects=projects)

@app.route('/certifications')
def certifications():
    return render_template('certifications.html', certifications=certifications)


if __name__ == '__main__':
    app.run(debug=True)

