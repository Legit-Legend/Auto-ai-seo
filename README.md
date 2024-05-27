# SEO Article Generator

This project is a Flask web application that generates SEO-optimized articles using OpenAI's GPT-4o model. It takes a target keyword, custom instructions, and URLs of relevant articles to create a comprehensive and well-structured blog post.

## Features

- Generate detailed blog post outlines using OpenAI's GPT-4o model.
- Extract text and outlines from given URLs.
- Combine multiple outlines into one comprehensive outline.
- Extract and utilize keywords for SEO optimization.
- Generate the final article in markdown format with specified word count and custom instructions.

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Steps

1. Clone the repository:
    ```sh
    git clone https://github.com/your-username/seo-article-generator.git
    cd seo-article-generator
    ```

2. Create a virtual environment and activate it:
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. Install the required packages:
    ```sh
    pip install flask requests beautifulsoup4 openai markdown
    ```

4. Set your OpenAI API key in the `app.py` file:
    ```python
    openai.api_key = 'your-api-key'  # Replace 'your-api-key' with your actual OpenAI API key
    ```

## Usage

1. Run the Flask application:
    ```sh
    python app.py
    ```

2. Open your web browser and navigate to `http://127.0.0.1:5000/`.

3. Fill out the form:
    - **Target Keyword:** Enter the main keyword for your blog post.
    - **Desired Word Count:** Adjust the slider to set the target word count for the article.
    - **Custom Instructions:** Provide any additional instructions for the article.
    - **Article URLs:** Enter the URLs of articles to be used for extracting outlines and keywords.

4. Click "Generate Article" to create the SEO-optimized blog post. The generated article will be displayed in the "Generated Article" section.

## Project Structure

- `app.py`: The main Flask application file.
- `templates/`: Directory containing the HTML template for the web interface.

## HTML Template

The HTML template (`templates/autoblogger html.html`) provides the user interface for the application. It includes a form for inputting the target keyword, word count, custom instructions, and URLs of relevant articles. The template also includes JavaScript for handling form submission and displaying progress steps.

## Contributing

Feel free to fork this repository and contribute by submitting pull requests. Any enhancements, bug fixes, or suggestions are welcome.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
