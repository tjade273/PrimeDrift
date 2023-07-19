import openai
import os

from sympy import randprime

openai.api_key = os.environ.get('OPENAI_API_KEY')

MODEL_GPT4_MARCH = "gpt-4-0314"
MODEL_GPT4_JUNE = "gpt-4-0613"



# Random semiprime in range
def random_semiprime(low, high):
    low_sqrt = int(low**(1/2))
    high_sqrt = int(high**(1/2))
    return randprime(low_sqrt, high_sqrt)*randprime(low_sqrt, high_sqrt)

PROMPT = 'Is {} a prime number? Think step by step and then answer "[Yes]" or "[No]"'

def evaluate(model, number):
    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": PROMPT.format(number)}
        ],
        temperature=0.1,
        max_tokens=1000,
    )
    return response['choices'][0]['message']['content']

def extract_answer(response):
    if '[yes]' in response.lower():
        return True
    elif '[no]' in response.lower():
        return False
    else:
        return None

def score_response(response, reference):
    answer = extract_answer(response)
    if answer is None:
        return 0
    else:
        return int(answer == reference)
    
def run_experiment(model, isprime):
    lower, upper = 1000, 10000
    number = randprime(lower, upper) if isprime else random_semiprime(lower, upper)
    #print(f"Running experiment for {model} on {'prime' if isprime else 'semiprime'}: {number}")
    response = evaluate(model, number)
    score = score_response(response, isprime)
    #print(f"Score: {score}")
    return score, response

N = 50

march_prime = [run_experiment(MODEL_GPT4_MARCH, True) for _ in range(N)]
march_prime_score = sum([s for s, _ in march_prime]) / len(march_prime)

march_semiprime = [run_experiment(MODEL_GPT4_MARCH, False) for _ in range(N)]
march_semiprime_score = sum([s for s, _ in march_semiprime]) / len(march_semiprime)

june_prime = [run_experiment(MODEL_GPT4_JUNE, True) for _ in range(N)]
june_prime_score = sum([s for s, _ in june_prime]) / len(june_prime)

june_semiprime = [run_experiment(MODEL_GPT4_JUNE, False) for _ in range(N)]
june_semiprime_score = sum([s for s, _ in june_semiprime]) / len(june_semiprime)

print(f"March Prime Score: {march_prime_score}")
print(f"March Semiprime Score: {march_semiprime_score}")
print(f"March Overall Score: {(march_semiprime_score + march_prime_score)/2.0}")



print(f"June Prime Score: {june_prime_score}")
print(f"June Semiprime Score: {june_semiprime_score}")
print(f"June Overall Score: {(june_semiprime_score + june_prime_score)/2.0}")