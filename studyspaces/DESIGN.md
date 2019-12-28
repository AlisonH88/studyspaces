### studyspaces design ###

We used flask to create our website so that the webpages could dynamically change based on the answers the user gave for the questionnaire. Each
page was created in a separate html file, and a layout html page was used as a general layout for each of the pages. A styles css file was used
to create general formatting across the pages as well. Then, there is one main python file that contains the app routes and SQL queries.

Each of the study spaces was stored in a SQL database. Within this database, we have a main table called places. We also have 4 other tables that
store the options for each question asked to the user. Each of these options is associated with an ID number that allows the program to match the
feature with a list of spaces. To provide the list of recommended study spaces, the program runs a SQL query to select spaces based on the features
from the database.

The static folder of our project contains each jpeg image of each study space, and also contains the style.css file.

The templates folder of our project contains all of our .html files. There is one file for each of the study spaces, as each of the study spaces have
a page containing information about them, and the folder also contains our homepage, layout page, welcome page, browse page, and a page for each question
asked to the user.

We used the Leaflet map service to plot the study spaces on a map. In addition, we used Leaflet to obtain the user's current location and to
then calculate the distance from the user to each study space.