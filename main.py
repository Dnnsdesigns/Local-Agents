# main.py

from fastapi import FastAPI, HTTPException, Depends, Security
from pydantic import BaseModel
from agents.web_research_agent import research_topic
from agents.blog_writer_agent import generate_blog_post
from agents.editor_agent import edit_text
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI(title="AI Agents API")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Mock user model and authentication (replace with real implementation)
class User(BaseModel):
    username: str
    is_active: bool

def fake_decode_token(token):
    return User(username="john_doe", is_active=True)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    user = fake_decode_token(token)
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    return user

# Authentication endpoint
@app.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    # Implement real authentication logic here
    return {"access_token": "fake-token", "token_type": "bearer"}

# Protected route example
@app.get("/users/me")
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

# Request and Response Models
class ResearchRequest(BaseModel):
    topic: str
    num_articles: int = 3

class ResearchResponse(BaseModel):
    summaries: list

class BlogRequest(BaseModel):
    topic: str
    outline: str = None
    style: str = "neutral"  # New parameter for style

class BlogResponse(BaseModel):
    blog_post: str

class EditRequest(BaseModel):
    blog_post: str
    instructions: str = "Improve grammar and clarity"

class EditResponse(BaseModel):
    edited_blog_post: str

class FullBlogProcessRequest(BaseModel):
    topic: str
    num_articles: int = 3

class FullBlogProcessResponse(BaseModel):
    research_summaries: list
    blog_post: str
    edited_blog_post: str

# API Endpoints

@app.post("/research", response_model=ResearchResponse)
async def research(request: ResearchRequest, current_user: User = Depends(get_current_user)):
    summaries = research_topic(request.topic, request.num_articles)
    if not summaries:
        raise HTTPException(status_code=404, detail="No summaries found.")
    return {"summaries": summaries}

@app.post("/generate_blog", response_model=BlogResponse)
async def generate_blog(request: BlogRequest, current_user: User = Depends(get_current_user)):
    blog_post = generate_blog_post(request.topic, request.outline, request.style)
    if not blog_post:
        raise HTTPException(status_code=500, detail="Failed to generate blog post.")
    return {"blog_post": blog_post}

@app.post("/edit_blog", response_model=EditResponse)
async def edit_blog(request: EditRequest, current_user: User = Depends(get_current_user)):
    edited_post = edit_text(request.blog_post, request.instructions)
    if not edited_post:
        raise HTTPException(status_code=500, detail="Failed to edit blog post.")
    return {"edited_blog_post": edited_post}

@app.post("/create_full_blog", response_model=FullBlogProcessResponse)
async def create_full_blog(request: FullBlogProcessRequest, current_user: User = Depends(get_current_user)):
    # Step 1: Research
    research_summaries = research_topic(request.topic, request.num_articles)
    if not research_summaries:
        raise HTTPException(status_code=404, detail="No research summaries found.")
    
    # Combine summaries for blog generation
    combined_summaries = "\n".join([f"{item['url']}: {item['summary']}" for item in research_summaries])
    
    # Step 2: Generate Blog Post
    blog_post = generate_blog_post(request.topic, combined_summaries, style="neutral")
    if not blog_post:
        raise HTTPException(status_code=500, detail="Failed to generate blog post.")
    
    # Step 3: Edit Blog Post
    edited_blog_post = edit_text(blog_post, "Improve grammar and clarity")
    if not edited_blog_post:
        raise HTTPException(status_code=500, detail="Failed to edit blog post.")
    
    return {
        "research_summaries": research_summaries,
        "blog_post": blog_post,
        "edited_blog_post": edited_blog_post
    }
