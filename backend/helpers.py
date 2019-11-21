def format_paginated_questions(questions):
    """Format paginated questions object."""
    results = []
    for question, category in questions:
        question = question.format()
        question["category_id"] = question["category"]
        question["category"] = category
        results.append(question)
    return results
