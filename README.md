# Capstone Project: Casting Agency

## Motivation for project

This is the Capstone Project in my Full Stack Developer course and is a requirement for completion.

The option I selected was to do the Casting Agency specification. This specification involved modeling a company that is responsible for creating movies and assigning actors to the movies. 

High-level features of this project include:

|   Endpoint  |                                               Description                                               |
|:-----------:|:-------------------------------------------------------------------------------------------------------:|
|    Movies   | Allows the addition, deletion and modification of a movie                                               |
|    Actors   | Allows the addition, deletion and modification of an actor                                              |
| Assignments | This endpoint assigns actors to movies. <br>Allows the addition, deletion and modification of an assignment |


**Notes:**
* This project is hosted on Heroku
* There is no front-end; only a back-end API
* Before using the API Endpoints below, [please login](https://ud-fsnd-capstone.herokuapp.com/) using one of the user accounts available in the Authentication section
* URL for Endpoints: https://ud-fsnd-capstone.herokuapp.com/ + {Endpoint}

## Project dependencies

All dependencies are listed in the `requirements.txt` file. 
Requirements can be installed by running `pip3 install -r requirements.txt`.

## Testing

Unit tests can be found in test_app.py. To run these tests locally, use `python3 test_app.py`.

## Authentication

There are three (3) main roles; each with different permissions for each endpoint. A user has been created for each role.

|        Role        |                                                     Permissions                                                     |                                  User Account                                 |
|:------------------:|:-------------------------------------------------------------------------------------------------------------------:|:-----------------------------------------------------------------------------:|
|  Casting Assistant | * Can view actors and movies                                                                                          | * Username: casting_assistant@capstone-test.com<br>* Password: assistant_password123 |
|  Casting Director  | * All permissions a Casting Assistant has and…<br>* Add or delete an actor / assignment from the database<br>* Modify actors, assignments or movies | * Username: casting_director@capstone-test.com<br>* Password: director_password123   |
| Executive Producer | * All permissions a Casting Director has and…<br>* Add or delete a movie from the database                              | * Username: executive_producer@capstone-test.com<br>* Password: producer_password123 |


## Endpoints

### GET '/movies'
- Fetches all movies available in the database
- Request Arguments: None
- Returns:

```
{
  "movies_list": "[list of movies]",
  "success": true
}
```

### POST '/movies'

- Inserts a new movie into the database
- Request Arguments:

```
{
  "title": "[movie title]",
  "release_date": "[release date]"
}
```

- Returns: 

```
{
  "id": "[id of inserted movie]",
  "title": "[title of inserted movie]",
  "release_date": "[release date of inserted movie]",
  "success": true
}
```

### DELETE '/movies/<int:id>'

- Deletes a movie by ID
- Request Arguments:

```
{
    "id": [id]
}
```

- Returns: 

```
{
  "deleted": [id of deleted movie],
  "success": true
}
```

### PATCH '/movies/<int:id>'

- Update an actor by ID
- Request Arguments:

```
{
  "id": [id],
  "title": "[updated title of movie]",
  "release_date": "[updated release date of movie]"
}
```

- Returns: 

```
{
  "id": [id of updated movie],
  "title": "[updated title of movie]",
  "release_date": "[updated release date of movie]"
  "success": true
}
```

### GET '/actors'
- Fetches all actors available in the database
- Request Arguments: None
- Returns:

```
{
  "actors_list": "[list of actors]",
  "success": true
}
```

### POST '/actors'

- Inserts a new movie into the database
- Request Arguments:

```
{
  "name": "[actor name]",
  "age": "[actor age]",
  "gender": "[gender]"
}
```

- Returns: 

```
{
  "id": "[id of inserted actor]",
  "name": "[name of inserted actor]",
  "age": "[age of inserted actor]",
  "gender": "[gender of inserted actor]",
  "success": true
}
```

### DELETE '/actors/<int:id>'

- Deletes an actor by ID
- Request Arguments:

```
{
    "id": [id]
}
```

- Returns: 

```
{
  "deleted": [id of deleted actor],
  "success": true
}
```

### PATCH '/actors/<int:id>'

- Update an actor by ID
- Request Arguments:

```
{
  "id": [id],
  "name": "[updated name of actor]",
  "age": "[updated age of actor]",
  "gender": "[updated gender of actor]"
}
```

- Returns: 

```
{
  "id": [id of updated actor],
  "name": "[updated name of actor]",
  "age": "[updated age of actor]",
  "gender": "[updated gender of actor]"
  "success": true
}
```

### GET '/assignments'
- Fetches all assignments in the database
- Request Arguments: None
- Returns:

```
{
  "assignments_list": "[list of assignments]",
  "success": true
}
```

### POST '/assignments'

- Inserts a new assignment into the database
- Request Arguments:

```
{
  "movie_id": "[movie id]",
  "actor_id": "[actor id]"
}
```

- Returns: 

```
{
  "id": "[id of inserted assignment]",
  "movie_id": "[movie id of inserted assignment]",
  "actor_id": "[actor id of inserted assignment]",
  "success": true
}
```

### DELETE '/assignments/<int:id>'

- Deletes an assignment by ID
- Request Arguments:

```
{
    "id": [id]
}
```

- Returns: 

```
{
  "deleted": [id of deleted assignment],
  "success": true
}
```