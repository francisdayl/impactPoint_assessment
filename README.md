# impactPoint_assessment
Technical assessment for Impact Point.
Pokémon Scouting Data Implementation.
## Description
Rest API with pokemon operations to showcase backend skills.
## Proyect Spefications
Check the requirements.txt <br>
**Python Version** 3.11 <br>
**Sqlite** For database <br>
**Flask** For backend framework <br>
**Black** For code formating <br>
**flask-marshmallow** For serialization and data validation <br>
**Flask-SQLAlchemy** For the ORM <br>
**Flask-Migrate** For migrations <br>
**polars** For data manipulation and creating the csv reports <br>
**Pytest** For testing <br>
**flask-swagger-ui** For api documentation, which uses the file ```/static/openapi_definition.yml``` that contains all the definitions. It has to be updated if making new changes to the api for keeping it up to date<br>


## How to Run
### Locally
0. Make sure you have python 3.11
1. Create a virtual environment
2. Activate the virtual environment
3. Install the dependencies
```
pip install -r requirements.txt
```
4. (If you are developing, for every change to the models you have to execute the following command, otherwise skip this step) Update the migrations
```
flask db migrate
```
5. Execute the migrations
```
flask db upgrade
```
6. Run
```
python run.py
```
### Docker
Build the docker image
```
docker build -t pokemon-scout .
```
Run the container in detached mode, mapping port 5000
```
docker run -d -p 5000:5000 --name pokemon-scout pokemon-scout
```

**Try the api**<br>
Visit: http://localhost:5000/api/docs/


# For testing