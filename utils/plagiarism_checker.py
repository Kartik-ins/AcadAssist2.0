from difflib import SequenceMatcher

def check_plagiarism(text):
    # Simulate checking against a sample database
    sample_texts = [
        "This is a sample text for plagiarism detection.",
        "Plagiarism is the act of using someone else's work without permission.",
        "EduAssist helps students manage their studies effectively."
    ]
    max_similarity = 0
    for sample in sample_texts:
        similarity = SequenceMatcher(None, text, sample).ratio()
        if similarity > max_similarity:
            max_similarity = similarity
    return round(max_similarity * 100, 2)