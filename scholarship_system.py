"""Student scholarship eligibility screener.

Computes a merit score from GPA and extracurricular credits, checks the
family income against a limit and saves the shortlist to a JSON file.
"""
import ast
import json
import operator

# Shared state (mutated in place, never rebound)
RESULTS = {}
CONFIG = {"merit_formula": "gpa * 10 + credits * 2"}
INCOME_LIMIT = 800000
CUTOFF = 85
MAX_GPA = 10.0

ALLOWED_OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}


def safe_eval(node, variables):
    """Evaluate a small arithmetic expression without using eval().

    Only numbers, the given variable names and + - * / are accepted.
    """
    if isinstance(node, ast.Expression):
        return safe_eval(node.body, variables)
    if isinstance(node, ast.Constant) and type(node.value) in (int, float):
        return node.value
    if isinstance(node, ast.Name) and node.id in variables:
        return variables[node.id]
    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        return ALLOWED_OPERATORS[type(node.op)](
            safe_eval(node.left, variables), safe_eval(node.right, variables))
    if isinstance(node, ast.UnaryOp) and isinstance(
            node.op, (ast.UAdd, ast.USub)):
        value = safe_eval(node.operand, variables)
        return value if isinstance(node.op, ast.UAdd) else -value
    raise ValueError("Unsupported element in merit formula")


def calculate_merit_score(gpa, credit_points):
    """Return the merit score for a GPA and extracurricular credit points."""
    tree = ast.parse(CONFIG["merit_formula"], mode="eval")
    return safe_eval(tree, {"gpa": gpa, "credits": credit_points})


def validate_scores(test_scores):
    """Return a list of problems found in an applicant's data."""
    problems = []
    gpa = test_scores.get("gpa")
    if not isinstance(gpa, (int, float)) or not 0 <= gpa <= MAX_GPA:
        problems.append(f"gpa must be between 0 and {MAX_GPA}")
    credit_points = test_scores.get("credits", 0)
    if not isinstance(credit_points, (int, float)) or credit_points < 0:
        problems.append("credits must be zero or more")
    income = test_scores.get("income")
    if not isinstance(income, (int, float)) or income < 0:
        problems.append("income is missing or negative")
    return problems


def evaluate_applicant(student_id, test_scores, logs=None):
    """Score one applicant, store the result and return eligibility."""
    if logs is None:
        logs = []
    problems = validate_scores(test_scores)
    if problems:
        RESULTS[student_id] = {"score": None, "eligible": False}
        logs.append(f"{student_id} rejected: {'; '.join(problems)}")
        return False
    score = calculate_merit_score(
        test_scores["gpa"], test_scores.get("credits", 0))
    eligible = score >= CUTOFF and test_scores["income"] < INCOME_LIMIT
    RESULTS[student_id] = {"score": score, "eligible": eligible}
    logs.append(f"{student_id} scored {score}")
    return eligible


def change_formula(new_formula):
    """Replace the merit formula if it is a safe arithmetic expression."""
    try:
        tree = ast.parse(new_formula, mode="eval")
        safe_eval(tree, {"gpa": 0, "credits": 0})
    except (SyntaxError, ValueError, ZeroDivisionError):
        print("Invalid merit formula, keeping the current one.")
        return
    CONFIG["merit_formula"] = new_formula


def persist_results(file="scholarships.json"):
    """Save the results to a JSON file."""
    with open(file, "w", encoding="utf-8") as handle:
        json.dump(RESULTS, handle)


def load_results(file="scholarships.json"):
    """Load results from a JSON file, keeping current ones on failure."""
    try:
        with open(file, encoding="utf-8") as handle:
            loaded = json.load(handle)
    except FileNotFoundError:
        print("No saved results found, starting empty.")
    except json.JSONDecodeError:
        print("Saved results file is corrupt, ignoring it.")
    else:
        RESULTS.clear()
        RESULTS.update(loaded)


def print_shortlist():
    """Print every applicant who is eligible for the scholarship."""
    print("Shortlisted applicants:")
    for student_id, result in RESULTS.items():
        if result["eligible"]:
            print(" ", student_id, "score =", result["score"])


def main():
    """Run the demo: evaluate sample applicants and print the shortlist."""
    logs = []
    evaluate_applicant(
        "U001", {"gpa": 9.1, "credits": 4, "income": 450000}, logs)
    evaluate_applicant(
        "U002", {"gpa": 7.2, "credits": 1, "income": 300000}, logs)
    evaluate_applicant(
        "U003", {"gpa": 12.5, "credits": -3, "income": -1}, logs)
    evaluate_applicant("U004", {"gpa": 6.5}, logs)
    formula = input("Merit formula (Enter to keep default): ")
    if formula:
        change_formula(formula)
    evaluate_applicant(
        "U005", {"gpa": 8.4, "credits": 3, "income": 600000}, logs)
    persist_results()
    load_results()
    print_shortlist()
    print("Evaluation log:")
    for entry in logs:
        print(" ", entry)


if __name__ == "__main__":
    main()
