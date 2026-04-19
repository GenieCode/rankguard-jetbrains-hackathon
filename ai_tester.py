# ai_tester.py
import sys
import os
from openai import OpenAI

# HARDCODE YOUR KEY HERE FOR THE HACKATHON DEMO ONLY
client = OpenAI(api_key="YOUR_KEY")


def generate_tests(file_path):
    with open(file_path, 'r') as f:
        code_content = f.read()

    prompt = f"""
        You are an expert QA engineer for Machine Learning, AdTech, and Ranking systems.
        Analyze the following Python code for a variant bidding model.
        Write a robust `pytest` suite that generates extreme, adversarial synthetic data to test edge cases (e.g., negative CTRs, missing dictionary keys, bizarre string inputs, or extreme float values).

        CRITICAL INSTRUCTION: Do not attempt to calculate the exact mathematical expected output for the assertions. Instead, assert that the function executes without crashing, returns a value of type float, and that the returned float is between 0.0 and 5.0.

        Return ONLY valid Python code. Do not include markdown formatting (like ```python) or any conversational text.

        Code to test:
        {code_content}
        """

    print("Analyzing variant bidding logic and generating adversarial synthetic data...")

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )

    test_code = response.choices[0].message.content.strip()

    if test_code.startswith("```python"):
        test_code = test_code[9:-3].strip()
    elif test_code.startswith("```"):
        test_code = test_code[3:-3].strip()

    dir_name = os.path.dirname(file_path)
    base_name = os.path.basename(file_path)
    test_file_name = f"test_adversarial_{base_name}"
    test_file_path = os.path.join(dir_name, test_file_name)

    with open(test_file_path, "w") as f:
        f.write(test_code)

    print(f"Success! Adversarial tests generated at: {test_file_path}")


if __name__ == "__main__":
    generate_tests(sys.argv[1])
