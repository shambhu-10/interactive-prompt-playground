import streamlit as st
import openai
import pandas as pd
from dotenv import load_dotenv
import os
from itertools import product

# Load environment variables
load_dotenv()

# Instantiate OpenAI client
client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_product_description(
    model,
    system_prompt,
    user_prompt,
    temperature,
    max_tokens,
    presence_penalty,
    frequency_penalty,
    stop_sequence=None
):
    """Generate a product description using OpenAI's API."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            temperature=temperature,
            max_tokens=max_tokens,
            presence_penalty=presence_penalty,
            frequency_penalty=frequency_penalty,
            stop=stop_sequence
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def main():
    st.title("🧪 Interactive Prompt Playground")
    st.write("Experiment with different OpenAI LLM parameters and observe their effects on product descriptions.")

    # Model selection
    model = st.selectbox("Select Model", ["gpt-3.5-turbo", "gpt-4o-mini"])

    # Prompt inputs
    system_prompt = st.text_area(
        "System Prompt",
        "You are a professional product description writer. Write concise, engaging product descriptions.",
        height=100
    )

    user_prompt = st.text_area(
        "User Prompt",
        "Write a product description for an iPhone 15 Pro.",
        height=100
    )

    # Optional stop sequences
    stop_input = st.text_input("Stop Sequence (optional, comma-separated)", "")
    stop_sequence = [s.strip() for s in stop_input.split(",")] if stop_input else None

    # Define parameter sets
    temperatures = [0.0, 0.7, 1.2]
    max_tokens_list = [50, 150, 300]
    presence_penalties = [0.0, 1.5]
    frequency_penalties = [0.0, 1.5]

    if st.button("Generate Descriptions"):
        with st.spinner("Generating responses from OpenAI..."):
            results = []

            for temp, tokens, pres_pen, freq_pen in product(
                temperatures, max_tokens_list, presence_penalties, frequency_penalties
            ):
                description = generate_product_description(
                    model,
                    system_prompt,
                    user_prompt,
                    temp,
                    tokens,
                    pres_pen,
                    freq_pen,
                    stop_sequence
                )
                results.append({
                    "Model": model,
                    "Temperature": temp,
                    "Max Tokens": tokens,
                    "Presence Penalty": pres_pen,
                    "Frequency Penalty": freq_pen,
                    "Description": description
                })

            # Convert to DataFrame
            df = pd.DataFrame(results)

            # Show in expanders
            st.subheader("📄 Generated Descriptions")
            for _, row in df.iterrows():
                with st.expander(
                    f"Temp: {row['Temperature']}, Tokens: {row['Max Tokens']}, "
                    f"Presence: {row['Presence Penalty']}, Frequency: {row['Frequency Penalty']}"
                ):
                    st.markdown(row["Description"])

            # Show Data Table
            st.subheader("📊 Tabular View")
            df["Short Description"] = df["Description"].apply(lambda x: x[:100] + "..." if len(x) > 100 else x)
            st.dataframe(df[["Model", "Temperature", "Max Tokens", "Presence Penalty", "Frequency Penalty", "Short Description"]])

            # Download as CSV
            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                "Download CSV",
                data=csv,
                file_name="generated_descriptions.csv",
                mime="text/csv"
            )

            # Reflection
            st.subheader("🧠 Analysis of Parameter Effects")
            st.markdown("""
            ### Temperature Effects
            - Lower temperatures (0.0) produce more focused and deterministic outputs.
            - Higher temperatures (1.2) result in more creative and varied responses.
            - A middle ground (0.7) offers balanced creativity and coherence.

            ### Token Length Effects
            - 50 tokens give short, crisp summaries.
            - 150 tokens offer detailed but readable outputs.
            - 300 tokens can deliver rich content but sometimes include repetition.

            ### Penalty Effects
            - *Presence Penalty* (1.5) encourages introducing new ideas.
            - *Frequency Penalty* (1.5) discourages repeating common phrases.
            - Combining both promotes originality and diversity of language.
            """)

if __name__ == "__main__":
    main()