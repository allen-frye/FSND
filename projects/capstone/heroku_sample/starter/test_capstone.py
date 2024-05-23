import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Person, Movies

# https://knowledge.udacity.com/questions/294099
DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTIzNzRkMWMzNTcyMDZkZTc2ZTciLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5OTM2NSwiZXhwIjoxNzE2NTg1NzY1LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImNyZWF0ZTptb3ZpZXMiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsInVwZGF0ZTphY3RvcnMiLCJ1cGRhdGU6bW92aWVzIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.tQf6La_VgZOg6h6oRKUYQ-QjlGRpaZreoR_ZpBMzpnTePYJk6Q7nrGMzkrTqrDMRA-flIjlxh0P9A7utoSX3iOWEJKabOb_3CALIJ1Et986L4-QgnIIBsHEsSgBI0dqPAoEvclWt8rMVlZBcJEDLppVr-RmX4CujOctizM1Ii8YVDWewXdIkpfi_1H7zwB7aw3WO1HTIkUVMw4gT7sFNrGZ6Zi-xfx1D0IeiYCcb2_knDnJ7VSl2DKNVKibPiGS15okKrCXjFmcax-Q4oJ2uRQqS2feuwxfixepZEw_0CNzUlX7lEvy4HsopuhcfIJaTdI3YSllBTx4nFb9A92v8Ng"
CASTING_DIRECTOR_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTFhZDRlNGNiNTg1OWZmYTZjZWIiLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5OTEwNiwiZXhwIjoxNzE2NTg1NTA2LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsiY3JlYXRlOmFjdG9ycyIsImRlbGV0ZTphY3RvcnMiLCJ1cGRhdGU6YWN0b3JzIiwidXBkYXRlOm1vdmllcyIsInZpZXc6YWN0b3JzIiwidmlldzptb3ZpZXMiXX0.0bBQg7OeNMWV9EaAeoJcMzAgRtkpn63DWK9ZAoY9YR2sz4G6geYJs7NhbI0V9mo_ZxgZLAMsCcuNC_eypuamyVF1rxWzoOlVNkvAWXkrHZ3V-lJpdRmVELgW-zCzxm6_sC_LKIbrDjfF5sTST0mQKLY-gqgqto8M4Ep80JQwvzcBhgyRN4wUhPXVrYr2AQKEoTcZ5RvygRZBEcF_aRC0NeOZYehi6ZH3eHZXz_qjBzZpZvtPCbmLdJCtSX1qs-BawbHXRY2zuFEd6THL9sYtsbkZy6BEqq3FOOL9jQ1toU9Yv97N3uUAQ6rvwBED3nDpTJ_NwdES8Ctt3gjmJKCeWg"
CASTING_AGENT_TOKEN = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkpWbFMyc1FwMUloYmFXVFRoUGp2ZCJ9.eyJpc3MiOiJodHRwczovL2Rldi15czJnam12OHQyaDdoMTZ0LnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NjRjZTFlZjJmODJlMzhmNmQ4YzQ4NDkiLCJhdWQiOiJodHRwczovL2FsbGVuLWZyeWUtY2Fwc3RvbmUtYXBwLWViMTViYjEzNDQ3Mi5oZXJva3VhcHAuY29tLyIsImlhdCI6MTcxNjQ5ODk1NiwiZXhwIjoxNzE2NTg1MzU2LCJzY29wZSI6IiIsImF6cCI6IjU5SGFGbFpESG82VUdFdVdyVjhLekhLVHd6cFI2UkU2IiwicGVybWlzc2lvbnMiOlsidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.phXfqUdc7k66DIAv-jITOyT3F1jdj4_FOAmd21ilK4qC--a8qH-LdgbudGTjG296uEuBuOT3Dev-e3-IqUYxW6hAP8NKNcIW7Z_Zuvb4k_H3hamfexjebMbLdG1zN7Hq5u4cecgjxL6mLDyRGT1kipRBS5XTL6pZXyq37L94YvUYrgmW_lsRl4FAocD620ppEUvQ8ePzD9Cp5NY00-mfs6PCbq9zcbAj9u-pzRyesimQ-djaYrFm1Ya_n6FEvm-tRNdbrVOmfwznyRIurolTsxthnwkN6l9bCSDv0wfNTk1UZOlYjCVLt0YdHthSZcBHoCXckpPARuJKlLRRRlChWQ"



def get_headers(token):
    return {'Authorization': f'Bearer {token}'}

class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgresql://postgres:[YOUR POSTGRES USER PASSWORD]@{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.new_actor = {
            'name': 'Steve Jobs',
            'age': '77',
            'catchprase': 'Think Different',
            'gender': 'Male'
            } 
        self.new_movie = {
            'title': 'Star Wars: The force awakens',
            'release_date': '03/05/2010'
            }   
        
        
        
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    


    def tearDown(self):
        """Executed after reach test"""
        pass

        """
        TODO
        Write at least one test for each test for successful operation and for expected errors.
        """
    def test_get_root(self):
        res = self.client().get("/")
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data))

   # GET

    def test_create_new_actor(self):
        auth_header = get_headers(DIRECTOR_TOKEN)
        res = self.client().post("/actors", headers=auth_header, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_create_new_actor_fail(self):
        auth_header = get_headers(DIRECTOR_TOKEN)
        res = self.client().post("/actors", headers=auth_header, json={})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_casting_agent_view_actors(self):
        auth_header = get_headers(CASTING_AGENT_TOKEN)
        res = self.client().get("/actors", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))
    
    def test_create_new_movie_fail_no_title(self):
        auth_header = get_headers(DIRECTOR_TOKEN)
        res = self.client().post("/movies", headers=auth_header, json={'release_date': '03/05/2010'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)

    def test_create_new_movie(self):
        auth_header = get_headers(DIRECTOR_TOKEN)
        res = self.client().post("/movies", headers=auth_header, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_casting_agent_view_actors(self):
        auth_header = get_headers(CASTING_AGENT_TOKEN)
        res = self.client().get("/movies", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(len(data))

    def test_patch_movie(self):
        auth_header = get_headers(CASTING_DIRECTOR_TOKEN)
        res = self.client().patch("/movies/3", headers=auth_header, json={'title': 'new_patched_movie', 'release_date': '05/23/2024'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
  
    def test_patch_actor(self):
        auth_header = get_headers(CASTING_DIRECTOR_TOKEN)
        res = self.client().patch("/actors/3", headers=auth_header, json={'name': 'my patched actor', 'age': '78', 'catchprase': 'nothing', 'gender': 'Male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    
    def test_patch_movie_fail(self):
        auth_header = get_headers(CASTING_DIRECTOR_TOKEN)
        res = self.client().patch("/movies/10000000000", headers=auth_header, json={'title': 'new_patched_movie', 'release_date': '05/23/2024'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
    
    def test_patch_artist_fail(self):
        auth_header = get_headers(CASTING_DIRECTOR_TOKEN)
        res = self.client().patch("/actors/10000000000", headers=auth_header, json={'name': 'my patched actor', 'age': '78', 'catchprase': 'nothing', 'gender': 'Male'})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_delete_actor_casting_agent(self):
        auth_header = get_headers(CASTING_AGENT_TOKEN)
        res = self.client().delete("/actors/6", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
      
    def test_delete_actor_casting_director(self):
        auth_header = get_headers(CASTING_DIRECTOR_TOKEN)
        res = self.client().delete("/actors/6", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    
    def test_delete_movie_casting_agent(self):
        auth_header = get_headers(CASTING_AGENT_TOKEN)
        res = self.client().delete("/movies/6", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
      
    def test_delete_actor_casting_director(self):
        auth_header = get_headers(DIRECTOR_TOKEN)
        res = self.client().delete("/movies/6", headers=auth_header)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
    
   

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()