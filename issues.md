# Software Engineering

## Lab 5

**Name:** Chirag Arun Yadwad  
**SRN:** PES2UG24CS136

---

# Static Code Analysis: Issue Log

File analysed: `scholarship_system.py` (line numbers refer to the original version).
Reports: `reports/before/` (original) and `reports/after/` (final).

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.69 / 10 (26 messages) | 10.00 / 10 |
| Bandit | 2 issues (1 Medium, 1 Low) | 0 issues |
| Flake8 | 12 violations | 0 violations |

## Issues found and fixed

| # | Issue | Type | Line(s) | Description | Fix Approach |
|---|-------|------|---------|-------------|--------------|
| 1 | Use of `eval()` on a user-editable string (B307, W0123) | Security (Medium) | 12, 24-26, 51-53 | `MERIT_FORMULA` can be replaced by whatever the user types at the prompt and is then run with `eval()`, so typing `__import__('os').system(...)` runs arbitrary code. | Replaced with `safe_eval()`, which parses the formula with `ast` and only allows numbers, the names `gpa` / `credits` and `+ - * /`. `change_formula()` validates a new formula first and rejects anything else. |
| 2 | Bare `except` with `pass` (B110, W0702, E722) | Bug / Security (Low) | 36-38 | Every error while loading results is silently swallowed, including a corrupt file, so data problems are hidden. | Catch only `FileNotFoundError` and `json.JSONDecodeError`, print a clear message, and keep existing results. |
| 3 | Mutable default argument (W0102) | Bug | 14 | `logs=[]` is created once and shared by every call, so log entries leak between calls. | Default is now `None`; a fresh list is created inside the function. `main()` passes its own list and prints it. |
| 4 | No input validation (found by running the program, no tool flags it) | Logic bug | 15-22, 47-50 | `U003` with GPA 12.5, credits -3 and income -1 is shortlisted with score 119. A missing income (`U004`) silently becomes 0, which always passes the income test. | Added `validate_scores()` (GPA 0-10, credits >= 0, income present and >= 0). Invalid applicants are recorded as not eligible and the reason is logged. |
| 5 | Files opened without `with` or encoding (R1732, W1514) | Bug (resource leak) | 29-31, 36 | `open()` is never closed if `write()` fails, and the encoding is platform dependent. | Use `with open(..., encoding="utf-8")` with `json.dump` / `json.load`. |
| 6 | `global` statements (W0603) | Design | 25, 34 | Functions rebind module globals, making state hard to follow and test. | State is held in `RESULTS` and `CONFIG` dicts that are mutated in place; no `global` needed. |
| 7 | Redefining built-in `credits` (W0622) | Style / Bug risk | 11, 16 | Parameter and local variable shadow the built-in `credits`. | Renamed to `credit_points` (the formula variable name `credits` is kept for users). |
| 8 | Unused imports `math`, `sys` (W0611, F401) | Style | 2-3 | Dead imports. | Removed. |
| 9 | Formatting: missing blank lines (E302, E305), line length (E501) | Style | 11, 14, 24, 28, 33, 40, 46, 59 | PEP 8 spacing violations. | Two blank lines around top-level definitions; long lines wrapped. |
| 10 | Comparison `== True` (E712, C0121) | Style | 43 | Redundant comparison to a boolean. | `if result["eligible"]:` |
| 11 | Missing docstrings (C0114, C0116) | Documentation | 1, 11, 14, 24, 28, 33, 40, 46 | No module or function docstrings. | Added docstrings everywhere. |
| 12 | `printShortlist` is not snake_case (C0103) | Naming | 40 | Violates PEP 8 naming. | Renamed to `print_shortlist`. |
| 13 | String `%` formatting (C0209) | Style | 21 | Old-style formatting. | Converted to f-strings. |
| 14 | `main()` runs on import | Design | 59 | Importing the module executes the program. | Added `if __name__ == "__main__":` guard. |

## Commits (one per tool)

1. `Fix Bandit findings` - issues 1 and 2.
2. `Fix Flake8 findings` - issues 8, 9 and 10.
3. `Fix Pylint findings` - issues 3-7 and 11-14.
