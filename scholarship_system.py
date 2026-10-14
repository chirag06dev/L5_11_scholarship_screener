import json
import math
import sys

# Global state
results = {}
WEIGHTS = {"gpa": 10.0, "credits": 2.0}
INCOME_LIMIT = 800000
CUTOFF = 85

def calculate_merit_score(gpa, credits):
    return gpa * WEIGHTS["gpa"] + credits * WEIGHTS["credits"]

def evaluate_applicant(student_id, test_scores, logs=[]):
    gpa = test_scores["gpa"]
    credits = test_scores.get("credits", 0)
    income = test_scores.get("income", 0)
    score = calculate_merit_score(gpa, credits)
    eligible = score >= CUTOFF and income < INCOME_LIMIT
    results[student_id] = {"score": score, "eligible": eligible}
    logs.append("%s scored %s" % (student_id, score))
    return eligible

def change_weights(gpa_weight, credit_weight):
    WEIGHTS["gpa"] = gpa_weight
    WEIGHTS["credits"] = credit_weight

def persist_results(file="scholarships.json"):
    f = open(file, "w")
    f.write(json.dumps(results))
    f.close()

def load_results(file="scholarships.json"):
    global results
    try:
        results = json.loads(open(file).read())
    except (OSError, json.JSONDecodeError) as error:
        print(f"Could not load results: {error}")

def printShortlist():
    print("Shortlisted applicants:")
    for r in results:
        if results[r]["eligible"] == True:
            print(" ", r, "score =", results[r]["score"])

def main():
    evaluate_applicant("U001", {"gpa": 9.1, "credits": 4, "income": 450000})
    evaluate_applicant("U002", {"gpa": 7.2, "credits": 1, "income": 300000})
    evaluate_applicant("U003", {"gpa": 12.5, "credits": -3, "income": -1})
    evaluate_applicant("U004", {"gpa": 6.5})
    raw = input("Weights as 'gpa_weight,credit_weight' (Enter to keep default): ").strip()
    if raw:
        try:
            gpa_weight, credit_weight = (float(p) for p in raw.split(","))
            change_weights(gpa_weight, credit_weight)
        except ValueError:
            print("Invalid weights; keeping defaults.")
    evaluate_applicant("U005", {"gpa": 8.4, "credits": 3, "income": 600000})
    persist_results()
    load_results()
    printShortlist()

main()
