import string

def  clean_tokenizer(text: str) -> list[str]:
    """
    This function takes a string as input and returns a
    list of tokens after cleaning the text.
    """
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = text.split()
    return text
print(clean_tokenizer("Hello, World! How are you?"))