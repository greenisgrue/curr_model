# curr_model

- Klona projektet med `git clone https://github.com/greenisgrue/map_kewords.git`
- Navigera till mappen map_kewords `cd map_kewords`
- Skapa ett virtual environment i python med `python3 -m venv venv`
- Aktivera venvsim med `source venv/bin/activate` för linux och Mac
- Aktivera med `venv\Scripts\activate.bat` för windows
- Installera dependecies med `pip3 install -r requirements.txt`
- Välj vilka två modeller du vill köra i gränssnittet genom `define_models.py`
- Kör gränssnittet med `python3 app.py`

# Gränssnittet
 1. Random ID hämtar slumpmässigt content från UR
 2. Topp 3 samt utstickare visas bland rekommenderat centralt innehåll
 3. Bedöm varje centralt innehåll med 'like', 'dislike' eller neutralt. Skicka ditt svar genom knappen submit under listorna. Neutralt svar fås genom att klicka i och sedan ur like eller dislike för en rekommendation.
4. Efter att ha skickat in sin bedömning återupprepas processen.
5. Alla svar sparas i MongoDB databas. Datan som sparas är: modelltyp, värdet på rekommendationen, rating (-1, 0, 1), content_id, 


