from fastapi import FastAPI, status
from app import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings
from fastapi.middleware.cors import CORSMiddleware


#---------------------IMPORTANT--------------------------------
# Remember to change ip for the WSL also in the database file!

"""
- We have to install sql driver which in our case is psycopg2, because sql alchemy cannot talk with the database on its own.
- Schema/pydantic models define structure of a request/response: so its for the validation,
- sqlalchemy models are responsible for creating query, deleting, uodating entries, defining columns in our tables,
- pydantic only knows how to deal with python dictionaries, so in order to override that we have to insert additional option class Config: orm_mode = True. Then, the SQLAlchemy model will be 
valid pydantic model,
- to the path parmeter we can add response_model = List[schemas.Post]
- JWT token: it contains header with the information about the used hashed function, the payload (for example user's id, user's role) and the signature which is the result of the hashed
 header, payload and the secret (password known only to the API). If someone changes sth in the payload, the signatre changes and we know that sth is broken.
 - query parameters: key value pairs (after the question mark); allow us to filter the result of the request: search=%20 this is the sign for space in the url
 - environment variables - not to hardcode
 - composite key; primary key that spans multiple columns
 - sqlalchemy cannot modify already created tables, we have to drop table, to update e.g. some column. That is why we are using tool alembic. It can be started by using alembic init alembic, 
 that creates folder alembic. Than we have to import our Base into env.py file(but the base must come from models.py, not from the database.py, because the models wont be read) in alembic folder, set metadata = BAse and in the alembic.ini change database sqlalchemy.url
 we are going to override value from the alembic.ini file with the 
 alembic --revision -m "message"

 when we are creating postgresql on ubuntu machine and accessing it from this machine we need to change ubuntu user to created postgres user, because local authentication will fail,
 we have to change postgres.conf and pg_hba file to remove peer authentication for local connections and change ip range to accept remote connections.
 to be able to connect pgadmin from my comp to the ubuntu  server i needed to add security rule to allow connections to the 5432 port on ubuntu machine (in the azure)
 - in the .env file in home directory we assign environment variables, then in .profile we create command to automatically create env var for us, after the machine reboot: 'set -o allexport; source /home/fastapi_ubuntu/.env; set +o allexport',
 - then we need to run alembic upgrade head,
 -  gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app --bind 0.0.0.0:8000,
 - we are going to run gunicorn in the background and during the reboot. The content of the gunicorn.service has to be copied to: (venv) fastapi_ubuntu@fastapi-ubuntu:/etc/systemd/system$ sudo nano api.service,
 - service doesnt have acccess to env variables (.profile), so we have to set: EnvironmentFile=/home/fastapi_ubuntu/.env,
 - nginx - high performance web server, serves as a proxy to our gunicorn: HTTPS Requests --> NGINX --> GUNICORN. SO the responsibility of SSL is taken by the NGINX, not our app. To allow nginx i had to open 80, 443 ports.
 - i have to created dns zone in azure and add my custom domain (devmro.site). Then i created a bunch od nameservers that i had to add to namecheap. I also created two sets in azure to point fastapi.devmro.site and www.fastapi.devmro.site to our vm ip,
 - we used certbot to generate SSL certificates,
 - firewall: we can use built in ufw to set rules:  sudo ufw status, sudo ufw allow ssh/http/https and 5432 (but it is not recommended, because someone can access our database using pgadmin, and we are hosting it om the same vitual machine, so..). Starting firewall sudo ufw enable,
 - docker: we are createing Dockerfile in our fastapi directory, assigning commands and then running docker build -t fastapi:1.0 /path/to/dockerfile,
 - instead of using docker run (CLI) we can use docker compose, the same functionality but in single file,
 - we want to create another container for our database, but we need to create volume, to allow data persistence after stopping the container.
 - if we want to push docker image to the remote repo, we need to rename the image with: sudo docker tag [source image] [new name],
 - then we need to sudo docker push [new_tag]. We also need to be logged in (sudo docker login)
 - its good to include two docker-compose files: for dev and production. But the we have to: sudo docker-compose -f docker-compose-prod.yml -d,
 - in the docker-compose we can use without the build: image
 """

# Thanks to alembic we dont need to use this command, alembic will create all necessary tables
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware, # funtion that runs before every request
    allow_origins=origins, # what domains should be able to talk to our API
    allow_credentials=True, # 
    allow_methods=["*"], # only specific HTTP methods (e.g. deny post methods and only allow get)
    allow_headers=["*"], #
    )


# routers allow us not to populate main file with different path operations
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/", status_code=status.HTTP_202_ACCEPTED) # this is endpoint; HTTP method: .get() request to our API, this is ("/")root path --> path operation
def root():
    return {"message": "Welcome to my API!!!!!!!!!!!"}


