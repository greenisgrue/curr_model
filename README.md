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


# Uppdatera modellen
1. Hämta all data i fetch_all_media eller data från ett valt tidsintervall genom fetch_media_time_interval. All data sparas i en CSV-fil
2. Kör modellen för valt content. Antingen allt, senaste 24 h eller valt tidsintervall. Metadata för content samt deras resultat i      modellen sparas i en dataframe som en pickle. 
3. Feedback från användare sparas i en databas. Modellen behöver hämta den datan och lägga i en self learning matrix där keywords får olika viktning i relation till centralt inneåhll baserat på användares feedback. För att uppdatera self learning matrix och få tillgång till all user feedback kör update_self_learning_matrix
4. För att uppdatera de sparade modellkörningarna på den uppdaterade self learning matrix kör get_recalculated_values
5. Nu ska allt vara uppdaterat och det är bara att köra vidare i gränssnittet!


