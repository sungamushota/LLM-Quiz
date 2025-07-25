# LLM Quiz Application

This is a simple web-based quiz application that uses an LLM to generate questions about the rail industry.

## Features

- Dynamically generated multiple-choice questions from an LLM.
- Flask backend with a simple frontend.
- Score tracking.

## Setup and Installation

Follow these steps to set up and run the application on your local machine.

### 1. Clone the Repository

```bash
git clone <repository-url>
cd LLM_Quiz
```

### 2. Create a Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
# For Windows
python -m venv .venv
.venv\Scripts\activate

# For macOS/Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies

Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

The application requires an OpenAI API key to function. Create a `.env` file in the root of the project directory:

```
OPENAI_API_KEY="your-openai-api-key-here"
```

Replace `"your-openai-api-key-here"` with your actual OpenAI API key.

### 5. Run the Application

Once the setup is complete, you can run the Flask application:

```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`.

## Logging

The application logs events to `logs/app.log`. This can be useful for debugging. #   L L M - Q u i z  
 