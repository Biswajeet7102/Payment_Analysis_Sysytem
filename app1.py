
from transformers import pipeline

zero_shot_classifier = pipeline("zero-shot-classification")

result = zero_shot_classifier(sequences="medicine prescription",
                              candidate_labels=['Transportation', 'Rent & Utilities', 'Travel', 'Medical', 'Loans',
                                                'General Services', 'Government + Non-Profit',
                                                'General Merchandise', 'Food & Drink', 'Entertainment',
                                                'Bank Transfers'], multi_class=True)

# Find the index of the label with the highest score
# Find and display the label with the highest score
max_score_label, max_score = max(zip(result["labels"], result["scores"]), key=lambda x: x[1])

print(f"{max_score_label}: {max_score}")
