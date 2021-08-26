# curr_model

- Klona projektet med `git clone https://github.com/greenisgrue/map_kewords.git`
- Navigera till mappen map_kewords `cd map_kewords`
- Skapa ett virtual environment i python med `python3 -m venv venv`
- Aktivera venvsim med `source venv/bin/activate` för linux och Mac
- Aktivera med `venv\Scripts\activate.bat` för windows
- Installera dependecies med `pip3 install -r requirements.txt`
- Kör gränssnittet med `python3 app.py`
- Hantera data genom att köra CLI med `python3 cli.py <funktion i cli.py> <parametrar>`

# Gränssnittet
 1. Random ID hämtar slumpmässigt content från UR
 2. Topp 3 samt utstickare visas bland rekommenderat centralt innehåll
 3. Bedöm varje centralt innehåll med 'like', 'dislike' eller neutralt. Skicka ditt svar genom knappen submit under listorna. Neutralt svar fås genom att klicka i och sedan ur like eller dislike för en rekommendation.
4. Efter att ha skickat in sin bedömning återupprepas processen.
5. Alla svar sparas i MongoDB databas. Datan som sparas är: modelltyp, värdet på rekommendationen, rating (-1, 0, 1), content_id, 


# Uppdatera data och modellen
1. Hämta all data i fetch_all_media eller data från ett valt tidsintervall genom fetch_media_time_interval (Kan endast köras om det redan finns). All data sparas i en CSV-fil i massive_data folder med samma namn som index. Efter "all" "all" för att hämta allt. Default limit är satt till 10000, sätt till 25000 för att hämta alla filmer. 
2. Feedback från användare sparas i en databas. Modellen behöver hämta den datan och lägga i en self learning matrix där keywords får olika viktning i relation till centralt inneåhll baserat på användares feedback. För att uppdatera self learning matrix och få tillgång till all user feedback kör update_self_learning_matrix. Första gången finns ingen self_learning_matrix som därför behöver skapas. Gör detta genom att köra funktionen reset_matrix i cli.py. 
3. Kör get_model_data för det index du vill, default är "search_ur_20210731". Antingen allt (skicka med parametrar "all" "all", ex. python3 cli.py get_model_data "all" "all"), senaste 24 h eller valt tidsintervall. Ex. "2021-06-02 04:00:00" "2021-08-02 04:00:00". Metadata för allt content samt deras resultat från modellen sparas i en dataframe som en pickle med namn model_pickle.pickle. Om du inte har någon pickle sparad (första gången eller om den raderas) behöver du skicka med False som parameter (python3 cli.py get_model_data "2021-08-02 04:00:00" "2021-08-02 05:00:00" False). Om en pickle finns låt default parameter True skickas med. Annars försvinner tidigare data från pickle. 
4. När ny feedback från användare kommit behöver de sparade modellkörningarna uppdateras för att viktningen från feedbacken ska tas med i score för centralt innehåll. För att göra detta, uppdatera först self learning matrix med update_self_learning_matrix och kör sedan get_recalculated_values. Den funktionen går igenom self_learning_matrix och uppdaterar viktningen för samtliga filmers centrala innehåll. 
5. Nu ska allt vara uppdaterat och det är bara att köra vidare i gränssnittet!

# Sammanfattningsvis, att hämta varje dygn:
1. I cli.py kör fetch_media_time_interval utan att sätta några parametrar.
2. I cli.py kör get_model_data. 
3. I cli.py kör update_self_learning_matrix och sedan get_recalculated_values. Inga parametrar behöver sättas.


