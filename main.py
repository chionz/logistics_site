from fastapi_pagination import add_pagination
import uvicorn
from fastapi.staticfiles import StaticFiles
import uvicorn, os
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse, HTMLResponse
from contextlib import asynccontextmanager
from fastapi import FastAPI, status
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.middleware.sessions import SessionMiddleware  

from api.utils.json_response import JsonResponseDict
from api.utils.logger import logger
from api.v1.routes import api_version_one, tracking
from api.utils.settings import settings

from api.db.database import create_database

#views Dependencies
from fastapi.responses import HTMLResponse
from api.utils.config import templates_env

from api.db.database import get_db as db
from api.v1.services.user import user_service


# Set up email templates and css static files
email_templates = Jinja2Templates(directory='api/core/dependencies/email/templates')

@asynccontextmanager
async def lifespan(app: FastAPI):
    #run_migrations()
    #create_database()
    yield

app = FastAPI(lifespan=lifespan)

origins = [
   "*"
]


app.add_middleware(SessionMiddleware, secret_key=settings.SECRET_KEY)
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_version_one)

@app.get("/health", tags=["API Health"])
async def get_root(request: Request) -> dict:
    return JsonResponseDict(
        message="Welcome to Logistics API", status_code=status.HTTP_200_OK, data={"URL": ""}
    )


# Root View
@app.get("/", response_class=HTMLResponse, tags=["Home"])
def index(request: Request):
    """main page"""
    try:
        user_id = user_service.fetch_user_refresh_token(request, db=db)
        isLogin = True if user_id else False
    except HTTPException as e:
        if e.status_code == 401:
            isLogin = False
        else:
            raise e 
    template = templates_env.get_template("index.html")
    return template.render({"request": request, "title": "Cartty Logistics", "isLogin": isLogin, "templates_env": templates_env})

@app.get("/about-us", response_class=HTMLResponse, tags=["About Us"])
def about(request: Request):
    """main page"""
    template = templates_env.get_template("about.html")
    return template.render({"request": request, "title": "About Us", "templates_env": templates_env})

@app.get("/contact-us", response_class=HTMLResponse, tags=["contact Us"])
def contact(request: Request):
    """main page"""
    template = templates_env.get_template("contact.html")
    return template.render({"request": request, "title": "contact Us", "templates_env": templates_env})

@app.get("/services", response_class=HTMLResponse, tags=["Services"])
def services(request: Request):
    """main page"""
    template = templates_env.get_template("services.html")
    return template.render({"request": request, "title": "About Us", "templates_env": templates_env})

@app.get("/track", response_class=HTMLResponse, tags=["About Us"])
def track(request: Request):
    """main page"""
    template = templates_env.get_template("track.html")
    return template.render({"request": request, "title": "Track Shipment", "templates_env": templates_env})

from fastapi import Depends
from api.db.database import get_db
from sqlalchemy.orm import Session
@app.get("/tracking/{track_number}", response_class=HTMLResponse, tags=["Track View"])
def index(request: Request, track_number:str, db: Session = Depends(get_db)):
    """main page"""
    try:
        user_id = user_service.fetch_user_refresh_token(request, db=db)
        isLogin = True if user_id else False
    except HTTPException as e:
        if e.status_code == 401:
            isLogin = False
        else:
            raise e 
    print("DEBUG DB URL:", os.getenv("DB_URL"))
    track = tracking.get_single_tracking(track_number, db)
    print(track)
    template = templates_env.get_template("main.html")

    return template.render(
        {
            "request": request,
            "title": "Title",
            "tag" : "Tracking",
            "page": "dashboard",
            "data": {"track": track, },
            "track": track,
            "templates_env": templates_env,
            "isLogin": True
        }
    )




app.mount("/static", StaticFiles(directory="static"), name="static")


# REGISTER EXCEPTION HANDLERS
@app.exception_handler(HTTPException)
async def http_exception(request: Request, exc: HTTPException):
    """HTTP exception handler"""

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "status": False,
            "status_code": exc.status_code,
            "message": exc.detail,
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception(request: Request, exc: RequestValidationError):
    """Validation exception handler"""

    errors = [
        {"loc": error["loc"], "msg": error["msg"], "type": error["type"]}
        for error in exc.errors()
    ]

    return JSONResponse(
        status_code=422,
        content={
            "status": False,
            "status_code": 422,
            "message": "Invalid input",
            "errors": errors,
        },
    )


@app.exception_handler(IntegrityError)
async def exception(request: Request, exc: IntegrityError):
    """Integrity error exception handlers"""

    logger.exception(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=400,
        content={
            "status": False,
            "status_code": 400,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


@app.exception_handler(Exception)
async def exception(request: Request, exc: Exception):
    """Other exception handlers"""

    logger.exception(f"Exception occured; {exc}")

    return JSONResponse(
        status_code=500,
        content={
            "status": False,
            "status_code": 500,
            "message": f"An unexpected error occurred: {exc}",
        },
    )


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000)) 

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
    #uvicorn.run("main:app", host="0.0.0.0", port=7001, reload=True)
