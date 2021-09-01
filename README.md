# Project Deployment
<img src="https://github.com/mdifils/deployment/blob/development/visuals/store_home_share.jpg">

## Description

The aim of this project is to be able to properly deploy a previously scrapped data set from the website Steam.
The data set was provided in a Json format. Because of this was required to converted in a cleaned way, to SQL. To do this purpose first it was needed to convert it into a pandas dataframe, and unravel all the nested dictionaries inside of the columns. Then, with the help of sqlalchemy we populated a table to format SQL. Futhermore we built relashions with between the main table and adjacent ones, such as price and pc requirements.
With this we could deploy locally with flaskmigrate plots related to this data set, as well as the table itself.
Finally in order to bring our work to the world we exposed it with Heroku, with the following web link: steam4u.herokuapp.com .


## Installation
* Python 3.8
* Jupyter notebook
* Trello
* Docker
* Heroku

## Databases 
This data was extracted from the Steam website. It can be founded on this link https://raw.githubusercontent.com/becodeorg/GNT-Arai-2.31/master/content/additional_resources/datasets/steam%20scrape/database.json?token=AUDYUGADWYEEUMWSRLY7VOLBHB5CI.


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
| file name                 | desc|
| file name                      | desc |
|file name                 | desc |
|file name      | file countaining .... |
| visuals            | Folder containing plots that are interesting and helped to bring insight as well as appealing pictures.  |


# Visuals  

* Below are some graphics present in our website:

<img src="https://github.com/mdifils/deployment/blob/development/visuals/newplot%20(2).png">


<img src="https://github.com/mdifils/deployment/blob/development/visuals/newplot.png">


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
