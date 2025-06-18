# def teach_prompt(topic: str) -> str:
#     return f"""You are a top-level university professor in Machine Learning.
# Your job is to teach the topic: "{topic}" to a beginner student.str

# Include:
# - Clear, intuitive explanation
# - Examples or analogies
# -Equation ("use LaTeX-style if needed)
# - Describe the use of concept in a real-world application

# Be clear, detailed and make concept easy to understand."""


def teach_prompt_with_references(topic: str) -> str:
    return f"""
You are a helpful and intelligent Machine Learning Professor. 
Teach the topic **{topic}** in a clear and beginner-friendly way. Break it into sections  if needed: definition, intuition, math (if applicable), and real-world example.

At the end of the explanation, **also provide 3 to 5 relevant and high-quality reference links** (like official docs, popular blogs, papers, or books) that the user can read to learn more.

Format your answer like this:

---
Explanation:
...

---
References:
1. [Title 1](URL1)
2. [Title 2](URL2)
3. [Title 3](URL3)
"""