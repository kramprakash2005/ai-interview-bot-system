import ollama
import json


# -----------------------------
# Evaluate Individual Answer
# -----------------------------
def evaluate_answer(question, answer):

    prompt = f"""
You are an AI interview evaluator.

Evaluate the candidate answer.

Question:
{question}

Answer:
{answer}

Score the answer from 1 to 10 based on:
- correctness
- depth of knowledge
- clarity of explanation

Also score communication ability from 1 to 10.

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

    response_text = response["message"]["content"].strip()

    # Remove markdown formatting if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        response_text = response_text.replace("json", "").strip()

    try:
        result = json.loads(response_text)
    except:
        result = {"score": 5, "communication": 5}

    return result


# -----------------------------
# Utility Average Function
# -----------------------------
def average(arr):

    if not arr:
        return 0

    return sum(arr) / len(arr)


# -----------------------------
# Generate Recruiter Report
# -----------------------------
def generate_report(scores, answers):

    transcript = ""

    for a in answers:
        transcript += f"""
Stage: {a['stage']}
Question: {a['question']}
Answer: {a['answer']}
"""

    prompt = f"""
You are a senior technical recruiter writing a candidate evaluation report.

Scores:
Technical Knowledge: {scores["technical_score"]}
Practical Knowledge: {scores["practical_score"]}
Behavioral Skills: {scores["behavioral_score"]}
Confidence: {scores["confidence_score"]}
Communication: {scores["communication_score"]}
Overall Score: {scores["overall_score"]}

Interview Transcript:
{transcript}

Write a detailed recruiter evaluation.

Return ONLY JSON in this format:

{{
"recommendation": "Hire or Consider or Reject",
"strengths": ["3-5 strengths"],
"weaknesses": ["2-3 weaknesses"],
"role_fit": "Explain how well the candidate fits the role",
"summary": "Short recruiter summary"
}}
"""

    response = ollama.chat(
        model="qwen2.5:7b",
        messages=[{"role": "user", "content": prompt}]
    )

    response_text = response["message"]["content"].strip()

    print("\nRaw LLM report response:\n")
    print(response_text)

    # Remove markdown code blocks if present
    if response_text.startswith("```"):
        response_text = response_text.split("```")[1]
        response_text = response_text.replace("json", "").strip()

    try:
        report = json.loads(response_text)
    except Exception as e:
        print("JSON parsing failed:", e)

        report = {
            "recommendation": "Consider",
            "strengths": ["Evaluation generated but parsing failed"],
            "weaknesses": ["Report parsing error"],
            "role_fit": "Unable to determine automatically",
            "summary": "The AI generated a report but JSON parsing failed."
        }

    return report


# -----------------------------
# Evaluate Entire Interview
# -----------------------------
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

    # Sectional Scores
    technical_score = average(scores["JD"])
    practical_score = average(scores["PROJECT"] + scores["INTERNSHIP"])
    behavioral_score = average(scores["BEHAVIORAL"])
    confidence_score = average(scores["INTRO"])
    communication_score = average(communication_scores)

    # Overall Score Calculation
    overall_score = (
        technical_score * 0.30
        + practical_score * 0.30
        + behavioral_score * 0.15
        + confidence_score * 0.15
        + communication_score * 0.10
    )

    score_report = {
        "technical_score": round(technical_score, 2),
        "practical_score": round(practical_score, 2),
        "behavioral_score": round(behavioral_score, 2),
        "confidence_score": round(confidence_score, 2),
        "communication_score": round(communication_score, 2),
        "overall_score": round(overall_score, 2)
    }

    # Generate recruiter report
    report = generate_report(score_report, answers)

    score_report["report"] = report

    return score_report