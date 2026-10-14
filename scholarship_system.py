"""Student scholarship eligibility screener."""
import json
import math
import sys

RESULTS = {}
WEIGHTS = {"gpa": 10.0, "credits": 2.0}
INCOME_LIMIT = 800000
CUTOFF = 85
MAX_GPA = 10.0

def calculate_merit_score(gpa, credit_points):
    """Return the merit score from GPA and extracurricular credits."""
    return gpa * WEIGHTS["gpa"] + credit_points * WEIGHTS["credits"]

def validate_applicant(test_scores):
    """Return (gpa, credits, income) or raise ValueError if data is invalid."""
    gpa = test_scores.get("gpa")
    credit_points = test_scores.get("credits", 0)
    income = test_scores.get("income")
    if gpa is None or not 0 <= gpa <= MAX_GPA:
        raise ValueError(f"gpa must be between 0 and {MAX_GPA}")
    if credit_points < 0:
        raise ValueError("credits cannot be negative")
    if income is None or income < 0:
        raise ValueError("income is required and cannot be negative")
    return gpa, credit_points, income

def evaluate_applicant(student_id, test_scores, logs=None):
    """Score an applicant, store the result and return eligibility."""
    if logs is None:
        logs = []
    gpa, credit_points, income = validate_applicant(test_scores)
    score = calculate_merit_score(gpa, credit_points)
    eligible = score >= CUTOFF and income < INCOME_LIMIT
    RESULTS[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible

def change_weights(gpa_weight, credit_weight):
    """Change the merit score weights."""
    WEIGHTS["gpa"] = gpa_weight
    WEIGHTS["credits"] = credit_weight

def persist_results(file_path="scholarships.json"):
    """Save results to a JSON file."""
    with open(file_path, "w", encoding="utf-8") as handle:
        handle.write(json.dumps(RESULTS))

def load_results(file_path="scholarships.json"):
    """Load results from a JSON file, if it exists and is valid."""
    try:
        with open(file_path, encoding="utf-8") as handle:
            loaded = json.load(handle)
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load results: {error}")
        return
    RESULTS.clear()
    RESULTS.update(loaded)

def print_shortlist():
    """Print all eligible applicants."""
    print("Shortlisted applicants:")
    for student_id, record in RESULTS.items():
        if record["eligible"] == True:
            print(" ", student_id, "score =", record["score"])

def submit(student_id, test_scores):
    """Evaluate an applicant and report invalid data instead of crashing."""
    try:
        evaluate_applicant(student_id, test_scores)
    except ValueError as error:
        print(f"Rejected {student_id}: {error}")

def main():
    """Run the screener."""
    submit("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    submit("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    submit("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    submit("U004", {"gpa": 6.5})
    raw = input("Weights as 'gpa_weight,credit_weight' (Enter to keep default): ").strip()
    if raw:
        try:
            gpa_weight, credit_weight = (float(p) for p in raw.split(","))
            change_weights(gpa_weight, credit_weight)
        except ValueError:
            print("Invalid weights; keeping defaults.")
    submit("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    print_shortlist()

main()