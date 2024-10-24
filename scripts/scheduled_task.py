# scripts/scheduled_task.py

import logging
from agents.web_research_agent import research_topic
from agents.blog_writer_agent import generate_blog_post
from agents.editor_agent import edit_text

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scheduled_blog_generation():
    topic = "Latest Trends in Machine Learning"
    num_articles = 3
    
    logger.info(f"Starting scheduled blog generation for topic: {topic}")
    
    # Step 1: Research
    research_summaries = research_topic(topic, num_articles)
    if not research_summaries:
        logger.error("No research summaries found.")
        return
    
    # Combine summaries for blog generation
    combined_summaries = "\n".join([f"{item['url']}: {item['summary']}" for item in research_summaries])
    
    # Step 2: Generate Blog Post
    blog_post = generate_blog_post(topic, combined_summaries)
    if not blog_post:
        logger.error("Failed to generate blog post.")
        return
    
    # Step 3: Edit Blog Post
    edited_blog_post = edit_text(blog_post, "Improve grammar and clarity")
    if not edited_blog_post:
        logger.error("Failed to edit blog post.")
        return
    
    # Here you can add code to publish the blog post, save it to a file, or send it via email
    logger.info("Scheduled blog post generated and edited successfully.")
    logger.info(f"Edited Blog Post:\n{edited_blog_post}")

if __name__ == "__main__":
    scheduled_blog_generation()
