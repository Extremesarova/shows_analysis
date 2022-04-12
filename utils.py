def get_page_type(page_name: str) -> str:
    if "отзывы и рецензии" in page_name:
        return "review"
    else:
        return "front"
