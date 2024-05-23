# Allen Frye Capstone Project

# Motivation for the project
This is a project for a production company to keep track of actors and the movies they have been in. It was needed due to the growth of the company and an inability to keep up with all actors and movies connected to the company.

## Production API URL
https://allen-frye-capstone-app-eb15bb134472.herokuapp.com/


## Project dependencies, local development and hosting instructions
Create a virtual environment for the project and run pip install -r requirement.txt. All dependencies should be created. The app uses the postgres database,  so you will need to add those credentials to an environment variable by running the command below in your virtual environment:

export DATABASE_URL="postgresql://postgres:[YOUR POSTGRES USER PASSWORD]@localhost:5432/postgres"

You will also need to run the command:

export EXCITED="true"

This is because after the first run I could not get the bash file setup.sh to run properly. 

After running the above commands, start the local server by running python3 app.py. 

## Postman 
Accessing the endpoints can be done via a postman collection included in the starter directory. The file is Capstone.postman_collection.json. Tokens will expire tomorrow.

## Endpont Documentation

http://localhost:5000/
Shows that the app is running. Should return json with a greeting variable: "!!!!! You are doing great in this Udacity project."

http://localhost:5000/coolkids
Returns: "Be cool, man, be coooool! You're almost a FSND grad!"

http://localhost:5000/response-url
Used for return page after token has been successfully issued

http://localhost:5000/authorization/url
Returns a url which can be used to generate new tokens. 

http://localhost:5000/actors - GET
Returns a list of all actors. 

http://localhost:5000/actors/ - POST
Adds a row in the People table. Expects the following JSON data: 

{
    'name': '',
    'catchphrase': '',
    'age': '',
    'gender': ''
}

http://localhost:5000/actors/[actor_id] - PATCH
Updates a row in the People table. Expects JSON above, and you can optionally pass in:

{
    'movies': '',
    'release_date": ''
}

Release date should be formatted as 00/00/0000.

This will add a movie to the Movies table and will add a relationship in the many-to-many table person_movie.

http://localhost:5000/actors/[actor_id] - DELETE
Deletes an actor from the People table. 

http://localhost:5000/movies - GET
Returns a list of all movies. 

http://localhost:5000/movies/ - POST
Adds a row in the Movies table. Expects the following JSON data: 

{
    'title': '',
    'release_date': ''
}

Release date should be formatted as 00/00/0000.


http://localhost:5000/movies/[movie_id] - PATCH
Updates a record in the Movies table. Send the same JSON as with POST method.

http://localhost:5000/movies/[movie_id] - DELETE
Deletes a movie from the Movies table. 

## User Roles and Permissions
Executive Producer
Can CRUD everything

Casting Director
Can CRUD actors. Can update movies.

Casting Agent
Can view movies and actors.


## Tokens
These are also included in the test_capstone.py file as variables.

EXECUTIVE_PRODUCER_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTIzNzRkMWMzNTcyMDZkZTc2ZTciLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5OTM2NSwiZXhwIjoxNzE2NTg1NzY1LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.tQf6La_VgZOg6h6oRKUYQ-QjlGRpaZreoR_ZpBMzpnTePYJk6Q7nrGMzkrTqrDMRA-flIjlxh0P9A7utoSX3iOWEJKabOb_3CALIJ1Et986L4-QgnIIBsHEsSgBI0dqPAoEvclWt8rMVlZBcJEDLppVr-RmX4CujOctizM1Ii8YVDWewXdIkpfi_1H7zwB7aw3WO1HTIkUVMw4gT7sFNrGZ6Zi-xfx1D0IeiYCcb2_knDnJ7VSl2DKNVKibPiGS15okKrCXjFmcax-Q4oJ2uRQqS2feuwxfixepZEw_0CNzUlX7lEvy4HsopuhcfIJaTdI3YSllBTx4nFb9A92v8Ng"

CASTING_DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTFhZDRlNGNiNTg1OWZmYTZjZWIiLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5OTEwNiwiZXhwIjoxNzE2NTg1NTA2LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.0bBQg7OeNMWV9EaAeoJcMzAgRtkpn63DWK9ZAoY9YR2sz4G6geYJs7NhbI0V9mo_ZxgZLAMsCcuNC_eypuamyVF1rxWzoOlVNkvAWXkrHZ3V-lJpdRmVELgW-zCzxm6_sC_LKIbrDjfF5sTST0mQKLY-gqgqto8M4Ep80JQwvzcBhgyRN4wUhPXVrYr2AQKEoTcZ5RvygRZBEcF_aRC0NeOZYehi6ZH3eHZXz_qjBzZpZvtPCbmLdJCtSX1qs-BawbHXRY2zuFEd6THL9sYtsbkZy6BEqq3FOOL9jQ1toU9Yv97N3uUAQ6rvwBED3nDpTJ_NwdES8Ctt3gjmJKCeWg"

CASTING_AGENT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTFlZjJmODJlMzhmNmQ4YzQ4NDkiLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5ODk1NiwiZXhwIjoxNzE2NTg1MzU2LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.phXfqUdc7k66DIAv-jITOyT3F1jdj4_FOAmd21ilK4qC--a8qH-LdgbudGTjG296uEuBuOT3Dev-e3-IqUYxW6hAP8NKNcIW7Z_Zuvb4k_H3hamfexjebMbLdG1zN7Hq5u4cecgjxL6mLDyRGT1kipRBS5XTL6pZXyq37L94YvUYrgmW_lsRl4FAocD620ppEUvQ8ePzD9Cp5NY00-mfs6PCbq9zcbAj9u-pzRyesimQ-djaYrFm1Ya_n6FEvm-tRNdbrVOmfwznyRIurolTsxthnwkN6l9bCSDv0wfNTk1UZOlYjCVLt0YdHthSZcBHoCXckpPARuJKlLRRRlChWQ"

### SETUP
I did not include the Auth0 Domain name, JWT signing secret, and the Auth0 Client ID in a Bash script as I was having trouble getting setup.sh to work after the first run. I was manually exporting the db url to run the app locally. In production everything works fine. 

### TESTING
For testing, a local database will need to be created named capstone_test. Credentials will need to be added to the test_capstone.py file in the variable self.database_path. 