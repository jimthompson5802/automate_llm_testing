###
# Minimal reproducible example for the ReliableCIRelevance grader NameError Exception
###
import textwrap

from judges.graders.relevance import ReliableCIRelevance

PROMPT = "provide a one paragraph summary of artificial intelligence"

REPSPONSE_TEXT = textwrap.dedent(
    """"
    Artificial Intelligence (AI) is a branch of computer science focused on creating machines that can perform tasks requiring human-like intelligence, \nsuch as learning, reasoning, problem-solving, perception, and language understanding. It encompasses a wide range of techniques, including machine \nlearning, neural networks, and deep learning, which enable systems to recognize patterns, make decisions, and improve over time. AI is applied across \nvarious fields, from healthcare and finance to robotics and entertainment, driving innovation and efficiency. While AI presents significant \nopportunities, it also raises ethical concerns related to bias, privacy, and job displacement, necessitating careful regulation and responsible \ndevelopment."
    """
)


evaluator = ReliableCIRelevance(model="gpt-4o")

evaluator.judge(PROMPT, REPSPONSE_TEXT)




