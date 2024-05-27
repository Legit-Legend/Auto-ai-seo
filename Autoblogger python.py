from flask import Flask, render_template, request, jsonify
import requests
from bs4 import BeautifulSoup
import openai
import markdown as md
import os

# Set your OpenAI API key here
openai.api_key = 'your-api-key'  # Replace 'your-api-key' with your actual OpenAI API key

# Initialize the Flask application
app = Flask(__name__)

def generate_outline(target_keyword, custom_instructions):
    """
    Generate an in-depth blog post outline using the OpenAI API.
    
    Parameters:
    - target_keyword: The main keyword for the blog post.
    - custom_instructions: Additional instructions for generating the outline.
    
    Returns:
    - The generated outline as a string.
    """
    prompt = f"""
    Your first task is to generate an in-depth and comprehensive blog post outline for an article about: "{target_keyword}"

    Please bear in mind the users {custom_instructions}

    Keep in mind that this is also the target keyword that we are trying to rank for so include it and variations of the keyword in the h1, h2, h3 and throughout the article.

    Please create an in-depth blog post outline with every single topic a person would have for this blog post topic. Include information specific to the topic you are writing about but also general information about the blog post topic that would be useful for readers. You are to write in an informative, simple tone in British English.
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant intended to create a high-quality SEO optimised outline to try to rank for the given keyword"},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def extract_text_from_url(url):
    """
    Extract the main text content from a given URL.
    
    Parameters:
    - url: The URL of the article to extract text from.
    
    Returns:
    - The extracted text as a string.
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        paragraphs = soup.find_all('p')
        article_text = ' '.join([para.get_text() for para in paragraphs])
        return article_text
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL: {e}")
        return ""

def extract_outline_from_article(article_text):
    """
    Extract an outline from a given article text using the OpenAI API.
    
    Parameters:
    - article_text: The text content of the article.
    
    Returns:
    - The extracted outline as a string.
    """
    prompt = f"""
    Please extract the main outline from this article:
    {article_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are an assistant intended to extract a SEO optimised outline from a specified URL."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def combine_outlines(outline1, outline2):
    """
    Combine two outlines into one comprehensive outline using the OpenAI API.
    
    Parameters:
    - outline1: The first outline.
    - outline2: The second outline.
    
    Returns:
    - The combined outline as a string.
    """
    prompt = f"""
    Ok now combine this final one to create one perfect outline targeting the keyword:
    {outline1}

    And:
    {outline2}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1000
    )
    return response.choices[0].message['content'].strip()

def extract_keywords(articles_text):
    """
    Extract keywords from a collection of article texts using the OpenAI API.
    
    Parameters:
    - articles_text: The combined text content of the articles.
    
    Returns:
    - The extracted keywords as a string.
    """
    prompt = f"""
    Extract the main keywords, target keywords, LSI keywords, and variations of the target keyword from the articles that you have looked at:
    {articles_text}
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=1500
    )
    return response.choices[0].message['content'].strip()

def generate_article(outline, keywords, word_count, custom_instructions):
    """
    Generate a comprehensive article based on an outline and keywords using the OpenAI API.
    
    Parameters:
    - outline: The outline of the article.
    - keywords: The keywords to include in the article.
    - word_count: The target word count for the article.
    - custom_instructions: Additional instructions for generating the article.
    
    Returns:
    - The generated article in markdown format as a string.
    """
    prompt = f"""
    Now utilising this outline generated:
    {outline}

    Write an in-depth, comprehensive and informative blog post with a target word count of {word_count}. Remember to include long paragraphs with in-depth knowledge on each outline. Always include list facts, tables and links where applicable. Always write in markdown format in British English. Also write in simple, easy to read human-like first-person style. Also include lists, tables, case studies, quotes, bolded words. Create a title as well keep in mind the target keyword, so include this keyword and variations of the keyword listed below in the h1, h2, h3 tags and naturally throughout the article. Make sure to include these keywords below naturally throughout the article:

    Keywords: {keywords}

    Please bear in mind the users {custom_instructions}

    Add links

    Please write this in markdown and include some relevant links on each topic make sure to embed them

    Add charts
    """
    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[
            {"role": "system", "content": "You are a professional copywriter specialized in creating SEO optimised content."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=3000
    )
    return response.choices[0].message['content'].strip()

@app.route('/')
def index():
    """
    Render the main page of the application.
    """
    return render_template('Article generation front end.html')

@app.route('/generate', methods=['POST'])
def generate():
    """
    Handle the generation of a blog post based on user input.
    """
    target_keyword = request.form['keyword']
    word_count = request.form['word_count']
    custom_instructions = request.form['custom_instructions']
    urls = request.form.getlist('urls')
    
    # Step 1: Generate initial outline
    initial_outline = generate_outline(target_keyword, custom_instructions)
    
    # Step 2: Extract outlines from articles
    outlines = []
    articles_text = ""
    for url in urls:
        article_text = extract_text_from_url(url)
        articles_text += article_text
        outline = extract_outline_from_article(article_text)
        outlines.append(outline)
    
    # Step 3: Combine outlines
    combined_outline = initial_outline
    for outline in outlines:
        combined_outline = combine_outlines(combined_outline, outline)
    
    # Step 4: Extract keywords
    keywords = extract_keywords(articles_text)
    
    # Step 5: Generate the final article
    final_article_markdown = generate_article(combined_outline, keywords, word_count, custom_instructions)
    
    return jsonify({
        'outline': combined_outline,
        'keywords': keywords,
        'article_markdown': final_article_markdown,
        'article_text': final_article_markdown  # Returning markdown directly
    })

if __name__ == '__main__':
    app.run(debug=True)
