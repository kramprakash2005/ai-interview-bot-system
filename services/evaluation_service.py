import ollama
import json


def evaluate_answer(question, answer):

    prompt = f"""
You are an interview evaluator.

Evaluate the candidate answer.

Question:
{question}

Answer:
{answer}

Score the answer from 1 to 10 based on:
- correctness
- depth of knowledge
- clarity of explanation

Also score communication ability.

Return ONLY JSON:

{{
"score": number,
"communication": number
}}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    try:
        result = json.loads(response["message"]["content"])
    except:
        result = {"score": 5, "communication": 5}

    return result


def average(arr):

    if not arr:
        return 0

    return sum(arr) / len(arr)


def evaluate_interview(answers):

    scores = {
        "JD": [],
        "PROJECT": [],
        "INTERNSHIP": [],
        "BEHAVIORAL": [],
        "INTRO": []
    }

    communication_scores = []

    for ans in answers:

        result = evaluate_answer(ans["question"], ans["answer"])

        score = result.get("score", 5)
        comm = result.get("communication", 5)

        stage = ans["stage"]

        if stage in scores:
            scores[stage].append(score)

        communication_scores.append(comm)

    technical_score = average(scores["JD"])

    practical_score = average(scores["PROJECT"] + scores["INTERNSHIP"])

    behavioral_score = average(scores["BEHAVIORAL"])

    confidence_score = average(scores["INTRO"])

    communication_score = average(communication_scores)

    overall_score = (
        technical_score * 0.30
        + practical_score * 0.30
        + behavioral_score * 0.15
        + confidence_score * 0.15
        + communication_score * 0.10
    )

    return {
        "technical_score": round(technical_score, 2),
        "practical_score": round(practical_score, 2),
        "behavioral_score": round(behavioral_score, 2),
        "confidence_score": round(confidence_score, 2),
        "communication_score": round(communication_score, 2),
        "overall_score": round(overall_score, 2)
    }