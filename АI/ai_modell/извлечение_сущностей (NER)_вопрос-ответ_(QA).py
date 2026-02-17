# Быстрая разведка: что умеют готовые модели?
ner = pipeline("ner")
qa = pipeline("question-answering")

# Если нужно обучать свою — шаги аналогичны:
# 1. AutoModelForTokenClassification (для NER)
# 2. AutoModelForQuestionAnswering (для QA)
# 3. Подготовка специального датасета
# 4. Trainer