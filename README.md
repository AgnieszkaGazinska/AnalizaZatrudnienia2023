## Charakterystyka oprogramowania

### a. Nazwa skrócona
Analiza zatrudnienia.

### b. Nazwa pełna
Aplikacja do analizy zatrudnienia w Polsce w 2023 roku.

### b. Cel aplikacji
Aplikacja umożliwia przegląd oraz analizę danych o zatrudnieniu i bierności zawodowej w Polsce w 2023 roku. Dane przedstawione są w ujęciu regionalnym – dla województw i miast wojewódzkich.
Przedstawiane są dane:
- pracujący według płci, wieku i wykształcenia,
- bierni zawodowo według wykształcenia.

---

## Prawa autorskie

### a. Autorzy:
Agnieszka Gazińska

### b. Warunki licencyjne:
Copyright (c) 2025 Agnieszka Gazińska

All Rights Reserved.

This software is proprietary and may not be copied, modified, distributed, or used in any way without the explicit permission of the author.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF, OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE..

### **Dane pobrane z repozytorium GitHub**

Dane geograficzne (pliki GeoJSON) użyte w aplikacji zostały pobrane z repozytorium GitHub dostępnego pod adresem:  
[https://github.com/ppatrzyk/polska-geojson](https://github.com/ppatrzyk/polska-geojson).

Te dane są udostępnione na licencji **MIT**, co oznacza, że mogą być używane, kopiowane, modyfikowane, łączone, publikowane, rozpowszechniane, sublicencjonowane i/lub sprzedawane, pod warunkiem, że w każdej kopii lub istotnej części danych zawarte będą informacje o prawach autorskich oraz licencji.
---

## Specyfikacja wymagań

### User Story 1: Wyświetlanie mapy Polski
Jako użytkownik chcę zobaczyć mapę Polski podzieloną na województwa i miasta wojewódzkie, aby móc analizować dane regionalne dotyczące zatrudnienia.

### User Story 2: Przeciąganie mapy
Jako użytkownik chcę mieć możliwość przesuwania mapy za pomocą myszki, aby móc dokładniej przeglądać wybrane regiony.

### User Story 3: Zoomowanie mapy
Jako użytkownik chcę móc przybliżać i oddalać mapę używając kółka myszy, aby skupić się na interesujących mnie obszarach.

### User Story 4: Klikanie na regiony
Jako użytkownik chcę kliknąć na województwo lub miasto wojewódzkie, aby uzyskać szczegółowe dane o zatrudnieniu.

### User Story 5: Zatrudnienie według płci
Jako użytkownik chcę zobaczyć dane dotyczące zatrudnienia kobiet i mężczyzn w wybranym regionie.

### User Story 6: Bierność zawodowa według wykształcenia
Jako użytkownik chcę zobaczyć wykres słupkowy bierności zawodowej według poziomu wykształcenia.

### User Story 7: Zatrudnienie według wykształcenia
Jako użytkownik chcę zobaczyć wykres zatrudnienia według poziomu wykształcenia.

### User Story 8: Zatrudnienie według wieku
Jako użytkownik chcę zobaczyć wykres zatrudnienia w różnych grupach wiekowych.

### User Story 9: Zamknięcie okna dashboardu
Jako użytkownik chcę wrócić do widoku głównego mapy po zamknięciu okna dashboardu.

### User Story 10: Obsługa braku danych
Jako użytkownik chcę zobaczyć komunikat o braku danych, gdy dane dla danego regionu są niedostępne.

### User Story 11: Zamknięcie aplikacji
Jako użytkownik chcę zamknąć aplikację, aby zakończyć korzystanie z niej.

---

## Architektura systemu / oprogramowania

### a. Architektura rozwoju

| Nazwa               | Przeznaczenie                                  | Wersja      |
|---------------------|------------------------------------------------|-------------|
| Visual Studio Code  | Edytor kodu źródłowego                         | 1.99.3      |
| Windows 11          | System operacyjny używany podczas tworzenia    | 24H2        |
| Python              | Język programowania                            | 3.13.3      |
| PyQt6               | Tworzenie GUI                                  | 6.9.0       |
| GeoPandas           | Obsługa danych przestrzennych (mapy)           | 1.0.1       |
| Pandas              | Przetwarzanie danych tabelarycznych (CSV)      | 2.2.3       |
| NumPy               | Obliczenia numeryczne                          | 2.2.5       |
| Matplotlib          | Tworzenie wykresów                             | 3.10.1      |
| Shapely             | Operacje na geometrii przestrzennej            | domyślna z GeoPandas |

**Dane źródłowe:**
- `wojewodztwa-max.geojson`
- `powiaty-medium.geojson`
- `biernosc_wykszt.csv`
- `zatr_wiek.csv`
- `zatr_wyksztalcenie.csv`
- `zatr_plec.csv`
  
---

### b. Architektura uruchomieniowa

| Nazwa               | Przeznaczenie                                  | Wersja      |
|---------------------|------------------------------------------------|-------------|
| Windows 11          | Docelowy system operacyjny                     | 24H2        |
| Python              | Środowisko uruchomieniowe                      | 3.13.3      |
| PyQt6               | GUI aplikacji                                  | 6.9.0       |
| GeoPandas           | Wyświetlanie i przetwarzanie map               | 1.0.1       |
| Pandas              | Wczytywanie danych CSV                         | 2.2.3       |
| NumPy               | Obsługa danych numerycznych                    | 2.2.5       |
| Matplotlib          | Rysowanie wykresów                             | 3.10.1      |

**Wymagane pliki:**
- `wojewodztwa-max.geojson`
- `powiaty-medium.geojson`
- `biernosc_wykszt.csv`
- `zatr_wiek.csv`
- `zatr_wyksztalcenie.csv`
- `zatr_plec.csv`
---

## Testy

### a. Scenariusze testów

1. **Test uruchomienia aplikacji**
   - Oczekiwany rezultat: Aplikacja otwiera się bez błędów.

2. **Test wyświetlania mapy**
   - Oczekiwany rezultat: Pokazuje się mapa Polski z podziałem na województwa i miasta wojewódzkie.

3. **Test przeciągania mapy**
   - Oczekiwany rezultat: Mapa przesuwa się podczas trzymania LPM.

4. **Test zoomowania**
   - Oczekiwany rezultat: Mapa przybliża się i oddala przy użyciu kółka myszy.

5. **Test kliknięcia na region**
   - Oczekiwany rezultat: Pokazują się dane dla klikniętego regionu.
  
6. **Test wykresu zatrudnienia według płci**
   - Oczekiwany rezultat: Wyświetla się wykres kołowy zatrudnionych według płci.
  
7. **Test wykresu zatrudnienia według wykształcenia**
   - Oczekiwany rezultat: Wyświetla się słupkowy wykres zatrudnionych według wykształcenia.

8. ** Test wykresu zatrudnienia według wieku**
   - Oczekiwany rezultat: Wyświetla się słupkowy wykres zatrudnionych według wieku.
     
9. **Test wykresu bierności zawodowej**
   - Oczekiwany rezultat: Wyświetla się słupkowy wykres bierności zawodowej według wykształcenia.

10. **Test zamknięcia okna dashboardu**
    - Oczekiwany rezultat: Po zamknięciu okna dashboardu, aplikacja wraca do widoku głównego mapy.
      
11. **Test komunikatu o braku danych**
   - Oczekiwany rezultat: Pokazuje się czytelny komunikat, gdy brak danych.

12. **Test zamknięcia aplikacji**
    - Oczekiwany rezultat: Po zamknięciu okna mapy, aplikacja zamyka się.

### b. Sprawozdanie z wykonania testów

| Test                                     | Status   | Uwagi                                 |
|------------------------------------------|----------|---------------------------------------|
| Uruchomienie aplikacji                   | ✅       | Bez błędów                            |
| Wyświetlanie mapy                        | ✅       | Poprawnie renderowana mapa            |
| Przeciąganie mapy                        | ✅       | Działa poprawnie                      |
| Zoomowanie mapy                          | ✅       | Reaguje na scroll                     |
| Kliknięcie na region                     | ✅       | Dane wczytywane prawidłowo            |
| Wykres zatrudnienia wg płci              | ✅       | Wykres rysuje się dynamicznie         |
| Wykres zatrudnienia wg wykształcenia     | ✅       | Wykres rysuje się dynamicznie         |
| Wykres zatrudnienia wg wieku             | ✅       | Wykres rysuje się dynamicznie         |
| Wykres bierności zawodowej               | ✅       | Wykres rysuje się dynamicznie         |
| Zamknięcie okna dashboardu               | ✅       | Okno zamyka się poprawnie             |
| Obsługa braku danych                     | ✅       | Wyświetla komunikat zgodnie z oczekiwaniem |
| Zamknięcie aplikacji                     | ✅       | Aplikacja zamyka się poprawnie        |

---

