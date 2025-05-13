import tkinter as tk
from tkinter import messagebox
import requests
import json

class AstrologyApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Astrology Divisional Charts")
        self.geometry("600x600")
        
        # Add a title label
        self.title_label = tk.Label(self, text="Astrology Divisional Charts", font=("Arial", 18))
        self.title_label.pack(pady=10)

        # Create buttons for different divisional charts
        self.create_chart_buttons()

        # Create a frame to show the chart data
        self.chart_frame = tk.Frame(self)
        self.chart_frame.pack(pady=20, fill=tk.BOTH, expand=True)

    def create_chart_buttons(self):
        # List of divisional charts (D1, D7, D10, D12, etc.)
        divisional_charts = ['d1', 'd7', 'd10', 'd12', 'd20', 'd24', 'd30', 'd40', 'd45', 'd60', 'd81', 'd144']
        for chart in divisional_charts:
            button = tk.Button(self, text=f"Load {chart.upper()} Chart", command=lambda chart=chart: self.load_chart(chart))
            button.pack(pady=5, fill=tk.X)

    def load_chart(self, chart_type):
        """Fetch the chart data from Flask API and display it in the GUI."""
        try:
            # Request data from the Flask API
            response = requests.get(f'http://127.0.0.1:5000/api/astronihar/{chart_type}')
            data = response.json()

            # Get the timestamp and chart data
            timestamp = data["timestamp_ist"]
            chart_data = data[f'{chart_type}_chart']

            # Clear previous chart data if any
            for widget in self.chart_frame.winfo_children():
                widget.destroy()

            # Display the chart data
            tk.Label(self.chart_frame, text=f"Generated at: {timestamp}", font=("Arial", 12)).pack()

            for planet, pdata in chart_data.items():
                planet_label = tk.Label(self.chart_frame, text=f"{planet}:")
                planet_label.pack(anchor="w", padx=10, pady=2)

                # Displaying the original sign, degree, and divisional sign
                tk.Label(self.chart_frame, text=f"Original Sign: {pdata['original_sign']}").pack(anchor="w", padx=20)
                tk.Label(self.chart_frame, text=f"Degree: {pdata['degree_decimal']}° ({pdata['degree_dms']})").pack(anchor="w", padx=20)
                tk.Label(self.chart_frame, text=f"{chart_type.upper()} Sign: {pdata[f'd{chart_type[1]}_sign']}").pack(anchor="w", padx=20)
                tk.Label(self.chart_frame, text="-" * 50).pack(anchor="w", padx=10, pady=5)

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Failed to fetch data: {e}")

# Create the application instance and run the app
if __name__ == "__main__":
    app = AstrologyApp()
    app.mainloop()
