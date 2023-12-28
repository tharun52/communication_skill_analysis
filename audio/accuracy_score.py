import difflib
import string

def tokenize_text(text):
    translator = str.maketrans("", "", string.punctuation)
    text_without_punctuation = text.translate(translator)
    tokens = text_without_punctuation.split()
    return tokens

def calculate_grammar_accuracy(correct_text, incorrect_text):
    correct_tokens = tokenize_text(correct_text)
    incorrect_tokens = tokenize_text(incorrect_text)

    differ = difflib.Differ()
    diff = list(differ.compare(correct_tokens, incorrect_tokens))

    correct_count = sum(1 for d in diff if d.startswith(' '))
    total_words = len(correct_tokens)
    
    accuracy_score = (correct_count / total_words) * 100 if total_words > 0 else 0

    return accuracy_score
