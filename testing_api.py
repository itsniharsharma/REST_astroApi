from flask import Flask, jsonify
import swisseph as swe
import datetime

# Instantiate the Flask app
app = Flask(__name__)

# Define your logic here
zodiac_signs = [
    'Aries', 'Taurus', 'Gemini', 'Cancer', 'Leo', 'Virgo',
    'Libra', 'Scorpio', 'Sagittarius', 'Capricorn', 'Aquarius', 'Pisces'
]

# Helper to convert decimal to DMS
def decimal_to_dms(degree_float):
    degrees = int(degree_float)
    minutes_float = (degree_float - degrees) * 60
    minutes = int(minutes_float)
    seconds = int((minutes_float - minutes) * 60)
    return f"{degrees}° {minutes}′ {seconds}″"

# Core data fetcher
def get_current_astro_data():
    latitude, longitude = 28.6139, 77.2090  # Delhi
    ist_now = datetime.datetime.now()
    utc_now = ist_now - datetime.timedelta(hours=5, minutes=30)
    swe.set_sid_mode(swe.SIDM_LAHIRI)

    jd = swe.julday(
        utc_now.year, utc_now.month, utc_now.day,
        utc_now.hour + utc_now.minute / 60 + utc_now.second / 3600
    )

    planets = {
        swe.SUN: 'Sun', swe.MOON: 'Moon', swe.MERCURY: 'Mercury',
        swe.VENUS: 'Venus', swe.MARS: 'Mars', swe.JUPITER: 'Jupiter',
        swe.SATURN: 'Saturn', swe.MEAN_NODE: 'Rahu'
    }

    planet_data = {}
    rahu_deg = 0

    for code, name in planets.items():
        pos, _ = swe.calc(jd, code, swe.FLG_SIDEREAL)
        deg = pos[0]
        zodiac = int(deg / 30)

        planet_data[name] = {
            'zodiac': zodiac_signs[zodiac],
            'degree_decimal': round(deg % 30, 5),
            'degree_dms': decimal_to_dms(deg % 30),
        }

        if name == 'Rahu':
            rahu_deg = deg

    # Ketu = 180° opposite Rahu
    ketu_deg = (rahu_deg + 180) % 360
    ketu_zodiac = int(ketu_deg / 30)
    planet_data['Ketu'] = {
        'zodiac': zodiac_signs[ketu_zodiac],
        'degree_decimal': round(ketu_deg % 30, 5),
        'degree_dms': decimal_to_dms(ketu_deg % 30)
    }

    return {
        'timestamp_ist': ist_now.strftime("%Y-%m-%d %H:%M:%S"),
        'planets': planet_data
    }

# Logic for divisional chart
def divisional_chart(sign_index, degree_in_sign, division_count, method='standard'):
    division_size = 30 / division_count
    division_index = int(degree_in_sign / division_size)

    if method == 'standard':
        return (sign_index + division_index) % 12
    elif method == 'even_odd':
        if (sign_index + 1) % 2 == 1:  # Odd signs
            return (sign_index + division_index) % 12
        else:  # Even signs
            return (sign_index + division_count - division_index) % 12
    elif method == 'cyclic':
        return (division_index) % 12
    return sign_index

# Generate divisional chart
def generate_divisional_chart(division_count, method):
    d1_data = get_current_astro_data()
    chart_data = {}

    for planet, pdata in d1_data['planets'].items():
        sign = pdata['zodiac']
        sign_index = zodiac_signs.index(sign)
        deg = pdata['degree_decimal']
        new_sign_index = divisional_chart(sign_index, deg, division_count, method)

        chart_data[planet] = {
            'original_sign': sign,
            'degree_decimal': deg,
            'degree_dms': pdata['degree_dms'],
            f'd{division_count}_sign': zodiac_signs[new_sign_index]
        }

    return {
        "timestamp_ist": d1_data["timestamp_ist"],
        f"d{division_count}_chart": chart_data
    }

# API Routes
@app.route('/api/astronihar/d1')
def d1_chart():
    return jsonify(get_current_astro_data())

@app.route('/api/astronihar/d7')
def d7_chart():
    return jsonify(generate_divisional_chart(7, method='even_odd'))

@app.route('/api/astronihar/d10')
def d10_chart():
    return jsonify(generate_divisional_chart(10, method='standard'))

@app.route('/api/astronihar/d12')
def d12_chart():
    return jsonify(generate_divisional_chart(12, method='standard'))

@app.route('/api/astronihar/d20')
def d20_chart():
    return jsonify(generate_divisional_chart(20, method='cyclic'))

@app.route('/api/astronihar/d24')
def d24_chart():
    return jsonify(generate_divisional_chart(24, method='standard'))

@app.route('/api/astronihar/d30')
def d30_chart():
    return jsonify(generate_divisional_chart(30, method='cyclic'))

@app.route('/api/astronihar/d40')
def d40_chart():
    return jsonify(generate_divisional_chart(40, method='standard'))

@app.route('/api/astronihar/d45')
def d45_chart():
    return jsonify(generate_divisional_chart(45, method='standard'))

@app.route('/api/astronihar/d60')
def d60_chart():
    return jsonify(generate_divisional_chart(60, method='cyclic'))

@app.route('/api/astronihar/d81')
def d81_chart():
    return jsonify(generate_divisional_chart(81, method='cyclic'))

@app.route('/api/astronihar/d144')
def d144_chart():
    return jsonify(generate_divisional_chart(144, method='cyclic'))

if __name__ == '__main__':
    app.run(debug=True)
