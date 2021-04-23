# Friss Storage
An API based project to upload/download files

## File Structure:
![alt file structure](friss_storage.png)

## Preconditions:
- Python 3

## Clone the project
```
git clone [git@github.com:richardf1981/friss_storage.git|https://github.com/richardf1981/friss_storage.git]
```

### Install dependencies
```
pip install -r requirements.txt
```

## Run local

### User for Basic Auth & JWT
For JWT its possible to freely create please go to 
/docs and press "try it out". Anyway a default user 
will be provided

### Install dependencies

```
pip install -r requirements.txt
```

### Run server

```
uvicorn app.main:app --reload
```

### Run unit tests

```
python -m unittest discover -s app/tests/unit
```

### Run integrated tests

```
python -m unittest discover -s app/tests/integrated
```

## Run with docker

### Build & Run server

```
docker-compose up -d --build
```


## API documentation (provided by Swagger UI)

```
http://127.0.0.1:8000/docs
```


### UI version
To see UI version please try this link
[http://localhost/](http://localhost/).

## Tasks
[ X ] API authenticated JWT <br>
[ X ] Storing data in database <br>
[ X ] Flexibility for changing Saving handling <br>
[ X ] Rest API <br>
[ X ] SPA for using API <br> 
[   ] Server side caching <br>
[ X ] Dockerfile <br>
[ X ] Logging for HTTP incoming requests <br>
[ X ] Verify setup (local) <br>
[ X ] Readme file <br>
[ X ] Unit tests <br>
[ X ] Integrated tests <br>
[   ] Concurrency tests using services <br>
[   ] Change DB Mechanism <br>
[ X ] Flake8: Pep8 Analyses + Manual review <br>
[   ] Refactor UI code JS <br>
[   ] Style UI <br>
[   ] Listing files available for download <br>

## Over Delivering
[ X ] APIs for user management JWT <br>
[   ] Running version in my private Cloud
