import csv
with open('results.csv', 'r') as f:
    reader = csv.DictReader(f)
    results = list(reader)

MODELS = ['gpt-3.5-turbo-0301', 'gpt-3.5-turbo-0613', 'gpt-4-0314', 'gpt-4-0613']

for model in MODELS:
    runs = [r for r in results if r['model'] == model]
    true_positive = 0
    false_positive = 0
    positive_n = 0

    true_negative = 0
    false_negative = 0
    negative_n = 0

    for run in runs:
        number, is_prime, score = run['number'], run['is_prime'], run['score']
        if is_prime == 'True':
            positive_n += 1
            if score == '1':
                true_positive += 1
            else:
                false_negative += 1
        else:
            negative_n += 1
            if score == '1':
                true_negative += 1
            else:
                false_positive += 1

    print(f"Model: {model}")
    print(f"Primes: {positive_n}, Composites: {negative_n}")
    print(f"Accuracy: {true_positive+true_negative}/{positive_n+negative_n} ({(true_positive+true_negative)/(positive_n+negative_n):.1%})")
    print()
    print(f"True Positive Rate: {true_positive}/{positive_n} ({true_positive/positive_n:.1%})")
    print(f"True Negative Rate: {true_negative}/{negative_n} ({true_negative/negative_n:.1%})")
    print()
    print()