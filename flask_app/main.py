from flask import Flask, render_template, request
from get_recommendations import get_recommendations

major_cities = ['', 'New York, New York', 'Los Angeles, California', 'Chicago, Illinois', 
				'Houston, Texas', 'Philadelphia, Pennsylvania', 'Pheonix, Arizona'
				'San Antonio, Texas', 'San Diego, California', 'Dallas, Texas', 
				'San Jose, California', 'Austin, Texas', 'Jacksonville, Florida',
				'San Francisco, California', 'Indianapolis, Indiana', 'Columbus, Ohio',
				'Fort Worth, Texas', 'Charlotte, North Carolina', 'Seattle, Washington',
				'Denver, Colorado', 'El Paso, Texas']

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("home.html", major_cities=major_cities)
    
@app.route('/results', methods=['POST', 'GET'])
def result():
    city = request.form['city']
    ref_city = request.form['reference_city']
    if not city:
    	return render_template("home.html")
    results = get_recommendations(city, ref_city)
    return render_template("results.html", major_cities=major_cities, table=results)

if __name__ == "__main__":
    app.run(debug=True)
