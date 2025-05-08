import sys
import geopandas as gpd
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from PyQt6.QtCore import Qt
from shapely.geometry import Point
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QDialog, QVBoxLayout, QGridLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class DashboardWindow(QDialog):
    def __init__(self, nazwa, dane_plec, dane_wykszt, dane_wiek, dane_bierni, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Dashboard dla {nazwa}")
        self.resize(1600, 800)
        grid_layout = QGridLayout()
        self.nazwa = nazwa
        self.dane_plec = dane_plec
        self.dane_wykszt = dane_wykszt
        self.dane_wiek = dane_wiek
        self.dane_biernosc = dane_bierni
        
        # Formatowanie nazw powiatów
        def format_nazwa(nazwa):
            words = nazwa.split()
            if words[0].lower() == "powiat" and len(words) > 1:
                words[1] = words[1].capitalize()
                for i in range(2, len(words)):
                    words[i] = words[i].capitalize()
            return " ".join(words)
        
        # Wykres kołowy - zatrudnienie wg płci
        fig1 = Figure(figsize=(6, 7))
        canvas1 = FigureCanvas(fig1)
        ax1 = fig1.add_subplot(111)

        # Dane do wykresu kołowego - zatrudnienie wg płci
        labels = ["kobiety", "mężczyźni"]
        try:
            kobiety = float(dane_plec.get('kobiety', 0))
            mezczyzni = float(dane_plec.get('mężczyźni', 0))
            if np.isnan(kobiety) or np.isnan(mezczyzni) or kobiety + mezczyzni == 0:
                raise ValueError("Niepoprawne dane")
            wszyscy = [kobiety, mezczyzni]

            def func(pct, wszyscy):
                wartosc = round(pct/100.*sum(wszyscy), 0)
                return f"{int(wartosc)} ({pct:.1f}%)"

            ax1.pie(
                wszyscy,
                labels=labels,
                autopct=lambda pct: func(pct, wszyscy),
                startangle=90,
                colors=["#ff69b4", "#87ceeb"]  # Różowy dla kobiet, niebieski dla mężczyzn
            )
            tytul = format_nazwa(nazwa)
            ax1.set_title(f"Pracujący według płci w: {tytul} w tys. osób")
            ax1.axis('equal')
            fig1.subplots_adjust(top=0.90)

        except Exception as e:
            print(f"Błąd podczas tworzenia wykresu dla {nazwa}: {e}")
            ax1.text(0.5, 0.5, "Brak danych", ha='center', va='center', fontsize=14)

        grid_layout.addWidget(canvas1,0,0)


        # Wykres słupkowy - zatrudnienie wg wykształcenia
        fig2 = Figure(figsize=(8, 6))
        canvas2 = FigureCanvas(fig2)
        ax2 = fig2.add_subplot(111)

        kolory = {
            "wyższe": "#0d47a1",
            "średnie ogólnokształcące": "#64b5f6",
            "policealne oraz średnie zawodowe/branżowe": "#bbdefb"
        }

        kolejnosc = [
                "wyższe",
                "średnie ogólnokształcące",
                "policealne oraz średnie zawodowe/branżowe"
            ]
        
        try:
            dane = dane_wykszt.copy()
            dane = dane[dane["wykształcenie"] != "ogółem"]
            dane = dane.set_index("wykształcenie").reindex(kolejnosc, fill_value=0).reset_index()
            
            os_x = list(range(len(kolejnosc)))

            dane_pelne =dane[dane["wartosc"] > 0]
            brak_danych = dane[dane["wartosc"] == 0]

            kolory_słupków = [kolory.get(w, "#cccccc") for w in dane_pelne["wykształcenie"]]
            x_slupki = [kolejnosc.index(w) for w in dane_pelne['wykształcenie']]
            slupki = ax2.bar(x_slupki, dane_pelne["wartosc"], color=kolory_słupków)
            
            # Etykiety z wartościami
            for slupek, wartosc in zip(slupki, dane_pelne["wartosc"]):
                ax2.text(slupek.get_x() + slupek.get_width()/2, slupek.get_height() + 1,
                        f"{wartosc:.1f}", ha='center', va='bottom', fontsize=6)

            # Informacja o braku danych
            for idx, row in brak_danych.iterrows():
                if row['wartosc'] == 0:
                    x = os_x[idx]
                    ax2.text(x, 1, "brak danych", ha='center', va='bottom', fontsize=8, color='gray')
            
            # Ustawienia osi
            ax2.set_title("Pracujący według wykształcenia")
            ax2.set_ylabel("tys. osób")
            ax2.set_xticks(os_x)
            ax2.set_xticklabels(dane["wykształcenie"], rotation=0, ha='center')
            ax2.tick_params(axis='x', labelsize=7)

            fig1.subplots_adjust(top=0.90)

        except Exception as e:
            print(f"Błąd wykresu wykształcenia: {e}")
            ax2.text(0.5, 0.5, "Brak danych", ha='center', va='center')

        grid_layout.addWidget(canvas2,0,1)
       

        # Wykres słupkowy - pracujący według wieku
        fig3 = Figure(figsize=(8, 7))
        canvas3 = FigureCanvas(fig3)
        ax3 = fig3.add_subplot(111)
        grupy_wiekowe = ["15-24", "25-54", "55-64", "65-89"]
        kolory_wiek = {
            "15-24": "#4db6ac",
            "25-54": "#00897b",
            "55-64": "#26a69a",
            "65-89": "#80cbc4"
        }

        try:
            dane = dane_wiek.copy()
            dane = dane[(dane["grupy"] != "ogółem")]
            dane = dane.set_index("grupy").reindex(grupy_wiekowe, fill_value=0).reset_index()
            os_x = list(range(len(grupy_wiekowe)))
            dane_pelne = dane[dane["wartosc"] > 0]
            brak_danych = dane[dane["wartosc"] == 0]

            # Słupki
            x_słupki = [grupy_wiekowe.index(w) for w in dane_pelne["grupy"]]
            kolory_słupków = [kolory_wiek.get(w, "#cccccc") for w in dane_pelne["grupy"]]
            bars = ax3.bar(x_słupki, dane_pelne["wartosc"], color=kolory_słupków)
            ax3.set_ylim(0, 100)

            # Etykiety wartości nad słupkami
            for bar, wartosc in zip(bars, dane_pelne["wartosc"]):
                ax3.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1,
                        f"{wartosc:.1f}%", ha='center', va='bottom', fontsize=6)

            # Brak danych
            for grupa in grupy_wiekowe:
                if grupa in brak_danych["grupy"].values:
                    x = grupy_wiekowe.index(grupa)
                    ax3.bar(x, 0, color='white')
                    ax3.text(x, 1, "brak danych", ha='center', va='bottom', fontsize=6, color='gray')

            # Ustawienia osi
            ax3.set_title("Pracujący według wieku")
            ax3.set_ylabel("% osób pracujących w danej grupie wiekowej")
            ax3.set_xticks(os_x)
            ax3.set_xticklabels(grupy_wiekowe, rotation=0, ha='center')
            ax3.set_yticks(range(0, 101, 20))
            ax3.tick_params(axis='x', labelsize=8)
            fig3.subplots_adjust(top=0.90)
            
        except Exception as e:
            print(f"Błąd wykresu wieku: {e}")
            ax3.text(0.5, 0.5, "Brak danych", ha='center', va='center')

        grid_layout.addWidget(canvas3,1,0)

        # Wykres słupkowy - bierni zawodowo według wykształcenia
        fig4 = Figure(figsize=(8, 7))
        canvas4 = FigureCanvas(fig4)
        ax4 = fig4.add_subplot(111)

        kolory_wykszt = {
            "wyższe": "#0d47a1",
            "średnie ogólnokształcące": "#64b5f6",
            "policealne oraz średnie zawodowe/branżowe": "#bbdefb",
            "zasadnicze zawodowe/branżowe": "#90caf9",
            "gimnazjalne, podstawowe i niższe": "#c5cae9"
        }

        kolejnosc = [
            "wyższe",
            "średnie ogólnokształcące",
            "policealne oraz średnie zawodowe/branżowe",
            "zasadnicze zawodowe/branżowe",
            "gimnazjalne, podstawowe i niższe"
        ]

        try:
            dane = dane_bierni.copy()
            dane = dane[dane['wykształcenie'] != 'ogółem']
            dane = dane.set_index("wykształcenie").reindex(kolejnosc, fill_value=0).reset_index()
            
            os_x = list(range(len(kolejnosc)))
            dane_pelne = dane[dane["wartosc"] > 0]
            brak_danych = dane[dane["wartosc"] == 0]

            x_slupki = [kolejnosc.index(w) for w in dane_pelne["wykształcenie"]]
            kolory_słupków = [kolory_wykszt.get(w, "#cccccc") for w in dane_pelne["wykształcenie"]]
            slupki = ax4.bar(x_slupki, dane_pelne["wartosc"], color=kolory_słupków)

            for slupek, wartosc in zip(slupki, dane_pelne["wartosc"]):
                ax4.text(slupek.get_x() + slupek.get_width()/2, slupek.get_height() + 0.3,
                        f"{wartosc:.1f}", ha='center', va='bottom', fontsize=5)

            # Dla braku danych
            for idx, row in brak_danych.iterrows():
                x = kolejnosc.index(row["wykształcenie"])
                ax4.bar(x, 0, color="#eeeeee", zorder=0)
                ax4.text(x, 1, "brak danych", ha='center', va='bottom', fontsize=5, color='gray')

            ax4.set_title("Bierność zawodowa według wykształcenia")
            ax4.set_ylabel("tys. osób")
            ax4.set_xticks(os_x)
            ax4.set_xticklabels(kolejnosc, rotation=8, ha='center')
            ax4.tick_params(axis='x', labelsize=5)
            fig4.subplots_adjust(top=0.90)

        except Exception as e:
            print(f"Błąd wykresu bierności: {e}")
            ax4.text(0.5, 0.5, "Brak danych", ha='center', va='center')

        grid_layout.addWidget(canvas4, 1, 1)


        self.setLayout(grid_layout)
        canvas1.draw()
        canvas2.draw()
        canvas3.draw()

class MapWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(10, 8))
        self.canvas = FigureCanvas(self.figure)
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        self.setLayout(layout)
        self.can_pan = False
        self._mouse_down_pos = None
        self._mouse_up_pos = None

        # Wczytanie danych
        self.wojewodztwa = gpd.read_file("wojewodztwa-max.geojson")
        self.powiaty = gpd.read_file("powiaty-medium.geojson")
        
        # Zatrudnienie wg płci
        self.df = pd.read_csv("zatr_plec.csv", sep=';')
        self.df.columns = self.df.columns.str.strip().str.lower()
        self.df['nazwa'] = self.df['nazwa'].astype(str).str.strip().str.lower()
        self.df['płeć'] = self.df['płeć'].str.strip().str.lower()
        self.df['wartosc'] = pd.to_numeric(self.df['wartosc'], errors='coerce')
        
        # Nazwy miast i województw
        miasta_wojewodzkie = [
            "Białystok", "Bydgoszcz", "Gdańsk", "Gorzów Wielkopolski", "Katowice",
            "Kielce", "Kraków", "Lublin", "Łódź", "Olsztyn", "Opole", "Poznań",
            "Rzeszów", "Szczecin", "Toruń", "Warszawa", "Wrocław", "Zielona Góra"
        ]
        nazwy_miast_woj = [f"powiat {miasto}" for miasto in miasta_wojewodzkie]
        self.miasta_wojewodzkie = self.powiaty[self.powiaty["nazwa"].isin(nazwy_miast_woj)]

        # Zatrudnienie płeć
        self.employment_data = {}
        grouped = self.df.groupby(['nazwa'])

        # Przekształcenie nazwy regionu z krotki na string
        for region, group in grouped:
            region_name = region[0]
            dane = {'kobiety': 0, 'mężczyźni': 0}  
            for _, row in group.iterrows():
                plec = row['płeć']
                if plec in ['kobiety', 'mężczyźni']:
                    dane[plec] = row['wartosc'] 
            if dane['kobiety'] != 0 and dane['mężczyźni'] != 0:
                self.employment_data[region_name.lower()] = dane 
        

        # Pracujący według wykształcenia
        self.df_wyksztalcenie = pd.read_csv("zatr_wyksztalcenie.csv", sep=';', dtype=str)
        self.df_wyksztalcenie.columns = self.df_wyksztalcenie.columns.str.strip().str.lower()
        self.df_wyksztalcenie['nazwa'] = self.df_wyksztalcenie['nazwa'].str.lower().str.strip()
        self.df_wyksztalcenie['wykształcenie'] = self.df_wyksztalcenie['wykształcenie'].str.strip().str.lower()
        self.df_wyksztalcenie['wartosc'] = pd.to_numeric(self.df_wyksztalcenie['wartosc'], errors='coerce')


        # Pracujący według wieku
        self.df_wiek = pd.read_csv("zatr_wiek.csv", sep=';', dtype = str)
        self.df_wiek.columns = self.df_wiek.columns.str.strip().str.lower()
        self.df_wiek['nazwa'] = self.df_wiek['nazwa'].str.lower().str.strip()
        self.df_wiek['grupy'] = self.df_wiek['grupy'].str.strip().str.lower()
        self.df_wiek['wartosc'] = pd.to_numeric(self.df_wiek['wartosc'], errors='coerce')
        

        # Bierni według wykształcenia
        self.df_bierni = pd.read_csv("biernosc_wykszt.csv", sep=";", dtype = str)
        self.df_bierni.columns = self.df_bierni.columns.str.strip().str.lower()
        self.df_bierni['wykształcenie'] = self.df_bierni['wykształcenie'].str.strip().str.lower()
        self.df_bierni['nazwa'] = self.df_bierni['nazwa'].str.lower().str.strip()
        self.df_bierni['wartosc'] = pd.to_numeric(self.df_bierni['wartosc'], errors='coerce')

        # Przeciąganie
        self._dragging = False
        self._last_mouse_pos = None

        # Zdarzenia interaktywne
        self.canvas.mpl_connect("scroll_event", self.zoom)
        self.canvas.mpl_connect("button_press_event", self.start_pan)
        self.canvas.mpl_connect("motion_notify_event", self.do_pan)
        self.canvas.mpl_connect("button_release_event", self.end_pan)
        self.plot_map()
    
    def plot_map(self):
        self.ax.clear()
        self.wojewodztwa.plot(ax=self.ax, edgecolor='black', facecolor='lightblue')
        self.miasta_wojewodzkie.plot(ax=self.ax, edgecolor='black', facecolor='darkblue', linewidth=0.2)
        self.wojewodztwa.boundary.plot(ax=self.ax, edgecolor='black', linewidth=0.8)
        self.ax.set_title("Polska - analiza zatrudnienia w województwach i miastach wojewódzkich dla 2023 roku")
        self.ax.axis("off")
        self.canvas.draw()

    def handle_click(self, event):
        if event.inaxes != self.ax or event.xdata is None or event.ydata is None:
            return

        if self._mouse_down_pos:
            dx = abs(event.xdata - self._mouse_down_pos[0])
            dy = abs(event.ydata - self._mouse_down_pos[1])
            if dx > 1 or dy > 1:  # jeżeli się przesunie, to nie traktuj jako kliknięcie
                return
        
        point = Point(event.xdata, event.ydata)

         # Sprawdź miasta (powiaty)
        for _, row in self.miasta_wojewodzkie.iterrows():
            if row['geometry'].contains(point):
                name = row['nazwa'].lower().strip()
                dane = self.employment_data.get(name)
                if dane:
                    self.open_dashboard(name.title(), dane)
                return
        # Sprawdź województwa
        for _, row in self.wojewodztwa.iterrows():
            if row['geometry'].contains(point):
                name = row['nazwa'].lower().strip()
                dane = self.employment_data.get(name)
                if dane:
                    self.open_dashboard(name.title(), dane)
                return

    # Otwarcie okna dashboardu
    def open_dashboard(self, nazwa, dane_plec):
        if isinstance(nazwa, tuple):
            nazwa = nazwa[0]
        nazwa = str(nazwa).strip().lower()

        # Filtrowanie danych o wykształceniu dla wybranego regionu
        dane_wykszt = self.df_wyksztalcenie[self.df_wyksztalcenie['nazwa'] == nazwa]

        # Filtrowanie danych o wieku dla wybranego regionu
        dane_wiek = self.df_wiek[self.df_wiek['nazwa'] == nazwa]

        # Filtrowanie danych o bierności zawodowej według wykształcenia dla wybranego regionu
        dane_bierni = self.df_bierni[self.df_bierni['nazwa'] == nazwa]
        # Przekazanie wszystkich danych do dashboardu
        dashboard_window = DashboardWindow(nazwa, dane_plec, dane_wykszt, dane_wiek, dane_bierni, self)
        dashboard_window.finished.connect(self.disable_pan)
        dashboard_window.exec()
    
    # Zablokowanie przeciągania mapy po zamknięciu okna dashboardu
    def disable_pan(self):
        self.can_pan = False

    # Zoomowanie mapy
    def zoom(self, event):
        base_scale = 1.2
        ax = self.ax
        xlim = self.ax.get_xlim()
        ylim = self.ax.get_ylim()
        xdata = event.xdata
        ydata = event.ydata

        if xdata is None or ydata is None:
            return

        if event.button == 'up':
            scale = 1 / base_scale
        elif event.button == 'down':
            scale = base_scale
        else:
            scale = 1

        new_width = (xlim[1] - xlim[0]) * scale
        new_height = (ylim[1] - ylim[0]) * scale

        relx = (xdata - xlim[0]) / (xlim[1] - xlim[0])
        rely = (ydata - ylim[0]) / (ylim[1] - ylim[0])

        new_xlim = [xdata - new_width * relx, xdata + new_width * (1 - relx)]
        new_ylim = [ydata - new_height * rely, ydata + new_height * (1 - rely)]

        self.ax.set_xlim(new_xlim)
        self.ax.set_ylim(new_ylim)
        self.canvas.draw()

    # Rozpoczęcie przeciągania po kliknięciu lewego przycisku myszy na mapie
    def start_pan(self, event):
        if event.button == 1 and event.xdata and event.ydata:
            self._dragging = True
            self._last_mouse_pos = (event.xdata, event.ydata)
            self._mouse_down_pos = (event.xdata, event.ydata)
            self.can_pan = True

    # Przesuwanie mapy po jej przeciągnięciu
    def do_pan(self, event):
        if self.can_pan and self._dragging and event.xdata and event.ydata:
            # Różnica przesunięcia myszy od ostatniej pozycji
            dx = self._last_mouse_pos[0] - event.xdata
            dy = self._last_mouse_pos[1] - event.ydata
            # Sprawdzenie granic mapy
            xlim = self.ax.get_xlim()
            ylim = self.ax.get_ylim()
            # Przesunięcie i ustawienie nowych limitów
            self.ax.set_xlim(xlim[0] + dx, xlim[1] + dx)
            self.ax.set_ylim(ylim[0] + dy, ylim[1] + dy)
            self.canvas.draw_idle()
            self._last_mouse_pos = (event.xdata, event.ydata)

    # Zakończenie przeciągania
    def end_pan(self, event):
        if event.button == 1:
            self._dragging = False
            if event.xdata is None or event.ydata is None or self._mouse_down_pos is None:
                return

            dx = abs(event.xdata - self._mouse_down_pos[0])
            dy = abs(event.ydata - self._mouse_down_pos[1])

            # Jeśli ruch był minimalny, traktuj jako klik
            if dx <= 1 and dy <= 1:
                self.handle_click(event)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Interaktywna Mapa Polski")
        self.map_widget = MapWidget(self)
        self.setCentralWidget(self.map_widget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

   