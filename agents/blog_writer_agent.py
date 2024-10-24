# agents/blog_writer_agent.py

from transformers import GPT2LMHeadModel, GPT2Tokenizer
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize the model and tokenizer (Replace with your custom model if available)
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
model = GPT2LMHeadModel.from_pretrained("gpt2")

def generate_text(prompt, max_length=500, temperature=0.7):
    """
    Generates text based on the provided prompt.
    """
    try:
        inputs = tokenizer.encode(prompt, return_tensors="pt")
        outputs = model.generate(
            inputs,
            max_length=max_length,
            temperature=temperature,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            early_stopping=True
        )
        text = tokenizer.decode(outputs[0], skip_special_tokens=True)
        logger.info("Generated blog post content")
        return text
    except Exception as e:
        logger.error(f"Error generating text: {e}")
        return ""

def generate_blog_post(topic, outline=None, style="neutral"):
    """
    Generates a blog post on a given topic, optionally using an outline and specifying style.
    """
    if outline:
        prompt = f"Write a detailed blog post on '{topic}' based on the following outline:\n{outline}\n\nBlog Post:"
    else:
        prompt = f"Write a detailed blog post on '{topic}'.\n\nBlog Post:"
    
    if style == "casual":
        prompt += "\n\nStyle: Write in a casual, conversational tone."
    elif style == "formal":
        prompt += "\n\nStyle: Write in a formal, professional tone."
    
    blog_post = generate_text(prompt)
    return blog_post
