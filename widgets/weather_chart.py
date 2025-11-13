# în widgets/weather_chart.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from datetime import datetime

class WeatherChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        
        # Creează figura și canvas-ul Matplotlib
        # Am setat culoarea de fundal să se potrivească cu tema ta întunecată
        self.figure = Figure(figsize=(5, 2), dpi=100, facecolor='#2B2B2B') 
        self.canvas = FigureCanvas(self.figure)
        
        # Adaugă un subplot (graficul efectiv)
        self.ax = self.figure.add_subplot(111)
        
        # Adaugă canvas-ul într-un layout
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        
        # Setează un aspect inițial
        self.setup_initial_chart()

    def setup_initial_chart(self):
        # Setează culorile pentru axă și text (pentru tema întunecată)
        self.ax.set_facecolor('#2B2B2B')
        self.ax.tick_params(axis='x', colors='white')
        self.ax.tick_params(axis='y', colors='white')
        self.ax.spines['bottom'].set_color('white')
        self.ax.spines['left'].set_color('white')
        self.ax.spines['top'].set_color('none')
        self.ax.spines['right'].set_color('none')
        
        self.ax.set_title("Evoluție Temperatură", color='white')
        self.ax.set_ylabel("°C", color='white')
        self.ax.grid(True, color='gray', linestyle='--')
        self.figure.tight_layout() # Aranjează frumos elementele
        self.canvas.draw()

    def update_plot(self, forecasts_list):
        """
        Primește lista de prognoze de la weather_service și actualizează graficul.
        """
        if not forecasts_list:
            return # Nu face nimic dacă nu avem date

        # Filtrăm datele: doar prognozele viitoare, maxim 24 de ore
        now = datetime.now(forecasts_list[0].time.tzinfo) # Păstrăm fusul orar
        upcoming_forecasts = [
            f for f in forecasts_list if f['time'] > now
        ][:24] # Luăm primele 24 de ore din viitor
        
        if not upcoming_forecasts:
            return

        # Extragem datele pentru plot
        temperatures = [f['temp'] for f in upcoming_forecasts]
        labels = [f['time'].strftime("%H:00") for f in upcoming_forecasts] # Ex: "14:00"
        
        # Curăță graficul vechi
        self.ax.clear()
        
        # Desenează graficul nou
        self.ax.plot(labels, temperatures, marker='o', linestyle='-', color='#007ACC')
        
        # Re-formatează axele (pentru tema întunecată)
        self.setup_initial_chart() # Re-aplică stilul
        self.ax.set_title("Evoluție Temperatură (urm. 24h)", color='white')
        self.ax.set_ylabel("°C", color='white')
        self.ax.set_xlabel("Ora", color='white')
        
        # Rotește etichetele de pe axa X pentru a fi lizibile
        self.figure.autofmt_xdate(rotation=45)
        self.figure.tight_layout()
        
        # Re-desenează canvas-ul
        self.canvas.draw()