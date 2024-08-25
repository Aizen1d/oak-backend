
# Oak Frontend

This is the backend for the oak assessment. I used FastAPI for the development. The code structure is simple and files names and folders are intuitive, separating logics for reusability.



## Techstack

- FastAPI
- SQLAlchemy for orm
- PyJWT for auth
- PostgreSQL for database
- Uvicorn web server
## Installation

```
  git clone https://github.com/Aizen1d/oak-backend.git

  cd oak-backend

  pip install -r requirements.txt

  uvicorn api:app --reload
```
    
## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`POSTGRES_URL`

`POSTGRES_PRISMA_URL`

`POSTGRES_URL_NO_SSL`

`POSTGRES_URL_NON_POOLING`

`POSTGRES_USER`

`POSTGRES_HOST`

`POSTGRES_PASSWORD`

`POSTGRES_DATABASE`

`LOCAL_FRONTEND`="http://127.0.0.1:3000"

`LOCALHOST_FRONTEND`="http://localhost:3000"

`PRODUCTION_FRONTEND`="https://oak-frontend1.vercel.app"

`JWT_SECRET`

`ALGORITHM`

`ACCESS_TOKEN_EXPIRE_MINUTES`