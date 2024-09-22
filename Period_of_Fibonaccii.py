def find_period(sequence):
    length = len(sequence)
    for p in range(3, length // 2 + 1):
        if sequence[:p] == sequence[p:2*p]:
            return p
    return None

def generate_sequence(k, max_length=10000):
    sequence = [1, 1]
    for n in range(2, max_length):
        next_term = (sequence[n-2] + sequence[n-1]) % k
        sequence.append(next_term)
    return sequence

def check_periodicity(k):
    sequence = generate_sequence(k)
    period = find_period(sequence)
    return period is not None

def main():
    for k in range(2, 1001):
        if check_periodicity(k) == False:
            print(f"The sequence does not have a period for k = {k}")
        else:
            print(f"The period of the sequence for k = {k} is {find_period(generate_sequence(k))}")

if __name__ == "__main__":
    main()