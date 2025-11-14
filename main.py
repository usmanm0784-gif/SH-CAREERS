from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import functions  # your MongoDB helper file
from models import User, userresult, config

app = FastAPI()

# Mount the 'static' directory
app.mount("/static", StaticFiles(directory="static", html=True), name="static")


# Set the 'templates' directory
templates = Jinja2Templates(directory="templates")

@app.get("/api/health")
def health():
    return {"status": "ok", "version": "1.0"}


#home route
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    greetings = "Welcome to SH CAREER!"
    return templates.TemplateResponse("index.html", {"request": request, "greetings": greetings})

#questions route
# --- /questions route ---
@app.get("/questions", response_class=HTMLResponse)
def show_questions(request: Request):
    data = functions.get_questions()

    # Check for error
    if "error" in data:
        raise HTTPException(status_code=500, detail=data["error"])

    # Render template with quiz data
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "questions": data["quiz"],           #  updated key
        "total_questions": data["total_questions"]
    })


#user route
@app.post("/add_user")
async def add_user_route(user: User):
    return functions.add_user_to_db(user)

#amin can see users
@app.get("/admin", response_class=HTMLResponse)
async def admin_page(request: Request):
    data = functions.get_users()  # already returns dict
    return templates.TemplateResponse("admin.html", {
        "request": request,
        "users": data["users"]
    })


@app.post("/result")
async def add_user_result_route(result: userresult):
    return functions.add_user_result_to_db(result)

# delete user by cnic
@app.delete("/delete_user/{cnic}")
async def delete_user(cnic: str):
    return functions.delete_user(cnic)


