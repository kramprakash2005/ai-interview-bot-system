import fitz


def extract_resume_text(file_path: str):

    text = ""

    try:

        with fitz.open(file_path) as doc:

            for page in doc:
                text += page.get_text()

    except Exception as e:

        print("Resume extraction error:", e)

    return text