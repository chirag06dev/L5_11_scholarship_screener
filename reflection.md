# Lab 5: Reflection

The handout does not list the reflection questions explicitly, so the four standard ones for this lab are answered below.

**1. Which tool was most useful and why?**
Pylint gave the most findings (26 messages) and the broadest view: it caught the mutable default argument, shadowed built-in, `global` usage, unclosed files and missing docstrings, and its score (4.69 to 10.00) gave a clear measure of progress. Bandit was the most important per finding: it reported only two issues, but the `eval()` one was a real code-execution hole. Flake8 was the quickest to fix and mostly mechanical (spacing and unused imports).

**2. Which issue was the most serious and how did you fix it?**
Using `eval()` on a formula that the user can type at the prompt. Anyone could run arbitrary Python through the scholarship screener. I replaced it with an `ast`-based evaluator that accepts only numbers, the names `gpa` and `credits`, and `+ - * /`, and validate new formulas before storing them. Rejected input is reported and the current formula is kept.

**3. What did static analysis not catch?**
Logic and data bugs. Applicant `U003` (GPA 12.5, negative credits, negative income) was shortlisted with score 119, and a missing income was silently treated as 0, which always passes the income check. None of the three tools flagged this; it only showed up by running the program and reading the output. I added `validate_scores()` for it. Static analysis checks how code is written, not whether it does the right thing.

**4. How does static analysis contribute to quality and maintainability?**
It gives fast, repeatable feedback without running the code, and enforces one consistent style, so reviews can focus on design. Docstrings, no global state, proper resource handling and meaningful names make the code easier to read, test and change. Running the tools in CI would stop these problems coming back. It complements, but does not replace, testing and code review.
