from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import functions  # your MongoDB helper file
from models import User, userresult, config

app = FastAPI()

# Mount the 'static' directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set the 'templates' directory
templates = Jinja2Templates(directory="templates")

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
        return templates.TemplateResponse("error.html", {
            "request": request,
            "message": data["error"]
        })

    # Render template with quiz data
    return templates.TemplateResponse("questions.html", {
        "request": request,
        "questions": data["quiz"],           # ✅ updated key
        "total_questions": data["total_questions"]
    })


#user route
@app.post("/add_user")
async def add_user_route(user: User):
    return functions.add_user_to_db(user)

@app.post("/result")
async def add_user_result_route(result: userresult):
    return functions.add_user_result_to_db(result)

