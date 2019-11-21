QUESTIONS_PER_PAGE = 10


def pagination(page, questions):
    """Paginate all questions."""
    results = []
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    for question, category in questions:
        question = question.format()
        question["category_id"] = question["category"]
        question["category"] = category
        results.append(question)
    paginated_results = results[start:end]
    return paginated_results
