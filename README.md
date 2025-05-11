# REST_astroApi


This project is a RESTful API built using **Flask** and **Swiss Ephemeris (swisseph)** that provides real-time astrological calculations based on the **sidereal Lahiri system**.

## 📌 Features

- Calculates the **Ascendant (Lagna)** along with zodiac sign, nakshatra, and pada.
- Computes the positions of 9 key planetary bodies: Sun, Moon, Mercury, Venus, Mars, Jupiter, Saturn, Rahu, and Ketu.
- Returns data in **JSON format** via a simple API endpoint.
- Uses **current IST timestamp** and the coordinates of **Delhi, India** by default.

## 🔧 Tech Stack

- **Python**
- **Flask** – for creating the web API
- **Swiss Ephemeris (swisseph)** – for astronomical calculations
- **datetime** – for managing IST and UTC time conversion

## 🚀 How It Works

- The API calculates the **Julian Day** for the current UTC time.
- Uses Swiss Ephemeris to compute the **Ascendant** and planetary longitudes.
- Converts degrees into corresponding **zodiac signs**, **nakshatras**, and **padas**.
- Returns the structured result as a JSON response.

## 📍 API Endpoint

### `GET /api/astronihar/d1`

Returns the current astrological data including:

- Timestamp in IST
- Ascendant details
- Planetary positions with zodiac, nakshatra, and pada

### Sample Response:
```json
{
  "timestamp_ist": "2025-05-11 18:30:00",
  "ascendant": {
    "zodiac": "Taurus",
    "degree": 12.34567,
    "nakshatra": "Rohini",
    "pada": 2
  },
  "planets": {
    "Sun": {
      "zodiac": "Aries",
      "degree": 25.6789,
      "nakshatra": "Bharani",
      "pada": 3
    },
  }
}
