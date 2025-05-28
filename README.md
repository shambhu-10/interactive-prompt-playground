# Interactive Prompt Playground

This project is a Streamlit app that allows you to experiment with different OpenAI LLM parameters and observe their effects on product descriptions.

## Setup

1. Clone the repository.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Create a `.env` file in the project directory with your OpenAI API key:
   ```
   OPENAI_API_KEY=sk-...
   ```
4. Run the Streamlit app:
   ```
   python -m streamlit run interactive_playground.py
   ```

## Features

- Select different OpenAI models (e.g., gpt-3.5-turbo, gpt-4o-mini).
- Customize system and user prompts.
- Experiment with various parameters like temperature, max tokens, presence penalty, and frequency penalty.
- View generated descriptions in a tabular format and download results as a CSV file.

## Note

This project uses the new OpenAI API interface (openai>=1.0.0). If you encounter any issues, ensure your `openai` package is up-to-date.

## Usage

1. Select your desired model (GPT-3.5-turbo or GPT-4o-mini)
2. Enter your system prompt and user prompt
3. Adjust the parameters using the sliders
4. Click "Generate" to see the results
5. View the grid of outputs and analysis

## Results Analysis

The application provides a comprehensive grid view of outputs across different parameter combinations, allowing you to observe how each parameter affects the generated text. A detailed analysis is provided below the grid, explaining the impact of each parameter on the output quality and characteristics.

## Security Note

This application is designed to handle API keys securely. Never commit your API key to the repository. Use environment variables or a secure configuration file to store your API key.