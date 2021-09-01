# Project Deployment
<img src="https://github.com/mdifils/deployment/blob/development/visuals/store_home_share.jpg">

## Description

The aim of this project is to be able to properly deploy scrapped data from the website Steam.
The data set was provided in a Json format. Because of this was required to converted in a cleaned way, to SQL. To do this purpose first it was needed to convert it into a pandas dataframe, and unravel all the nested dictionaries inside of the columns. Then, with the help of sqlalchemy we populated a table to format SQL. Futhermore we built relashions between the main table and an adjacent one, namely price.
With this we could deploy locally, with flaskmigrate, two plots related to this data set, as well as the table itself.
It was used some HTML code to make the website more user friendly and appealing.
We also scrapped more then 40000 url's from each game in order to add more information about them. In a second fase, we were able to futher gather information over 3000.
Finally in order to bring our work to the world we exposed it with Heroku, with the following web link: steam4u.herokuapp.com .


## Installation
* Python 3.8
* Jupyter notebook
* Trello
* Docker
* Heroku

## Databases 
The data was scrapped from the Steam website. It can be founded on it's raw format on the following link: https://raw.githubusercontent.com/becodeorg/GNT-Arai-2.31/master/content/additional_resources/datasets/steam%20scrape/database.json?token=AUDYUGADWYEEUMWSRLY7VOLBHB5CI .

Regarding the SQL format, the data can be found on this link: http://steam4u.herokuapp.com/view .


## Packages used
* Pandas
* Sqlite
* Flaskmigrate
* Sqlalchemy
* Plotly
* Matplotlib
* json  


# Usage
| File                        | Description                                                     |
|-----------------------------|-----------------------------------------------------------------|
| migrations            | Interections with flaskmigrate.|
| static          | Folder with the files to be used in the html templates. |
|templates                | html code|
|.gitignore     | Contains name of files to be ignored in the repository. |
|data.db    | sql tabel|
| df_cleaning.py       | python file with code that cleans the dataframe |
|Dockerfile  |Docker file with code to build an image.|
| loading_data.py       | Python file with code that populates the SQL tabel.  |
| model.py         |Python file with code that relates the table to the local server. |
|Procfile  |File to deploy with Heroku.|
| README.md    |Text file with short description if the project. |
| requirements.txt     |Text file requeried to deploy with docker.|
|scrapping.py  |Python file with code to scrape extra information about the games. |
| steam_game.py    |Python file with code to creat the application. |

# Visuals  

* Below are some graphics present in our website:

<img src="https://github.com/mdifils/deployment/blob/development/visuals/newplot%20(2).png">


<img src="https://github.com/mdifils/deployment/blob/development/visuals/newplot.png">


## Problems encountered
Our main goal initially was to have only one SQL table with all the information. As the project progressed, we realized that including relational tabels would be a great add on. Because of doing it in a later process of our project, we could only inclued an extra tabel, being 'Price'. We were going to inclued pc requirements, but this had to be left out because of some improper funtion building with regex.



## Final words

Deploying is an important step in being able to expose one's work to the world.
In this situation, this project brought better insight over dealing with SQL, manipulating Json files, deploying locally thought python libraries, and understanding Docker and Heroku. Html was also important to get some basic concepts.


# Contributors
| Name                  | Github                                 |
|-----------------------|----------------------------------------|
|Leonor Drummonnd      | https://github.com/ltadrummond              |
|Bilal Mesmoudi  | https://github.com/BMesm    |
|Michel Ombessa  | https://github.com/mdifils    |
|Jacques Declercq | https://github.com/JacquesDeclercq      |



# Timeline
26/08/2021 - 01/09/2021
