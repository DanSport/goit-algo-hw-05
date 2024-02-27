import timeit

# Алгоритм Боєра-Мура
def build_shift_table(pattern):
    table = {}
    length = len(pattern)
    for index, char in enumerate(pattern[:-1]):
        table[char] = length - index - 1
    table.setdefault(pattern[-1], length)
    return table

def boyer_moore_search(text, pattern):
    shift_table = build_shift_table(pattern)
    i = 0
    while i <= len(text) - len(pattern):
        j = len(pattern) - 1
        while j >= 0 and text[i + j] == pattern[j]:
            j -= 1
        if j < 0:
            return i
        i += shift_table.get(text[i + len(pattern) - 1], len(pattern))
    return -1

# Алгоритм Кнута-Морріса-Пратта
def compute_lps(pattern):
    lps = [0] * len(pattern)
    length = 0
    i = 1
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(main_string, pattern):
    M = len(pattern)
    N = len(main_string)
    lps = compute_lps(pattern)
    i = j = 0
    while i < N:
        if pattern[j] == main_string[i]:
            i += 1
            j += 1
        elif j != 0:
            j = lps[j - 1]
        else:
            i += 1
        if j == M:
            return i - j
    return -1

# Алгоритм Рабіна-Карпа
def polynomial_hash(s, base=256, modulus=101):
    n = len(s)
    hash_value = 0
    for i, char in enumerate(s):
        power_of_base = pow(base, n - i - 1) % modulus
        hash_value = (hash_value + ord(char) * power_of_base) % modulus
    return hash_value

def rabin_karp_search(main_string, substring):
    substring_length = len(substring)
    main_string_length = len(main_string)
    base = 256
    modulus = 101
    substring_hash = polynomial_hash(substring, base, modulus)
    current_slice_hash = polynomial_hash(main_string[:substring_length], base, modulus)
    h_multiplier = pow(base, substring_length - 1) % modulus
    for i in range(main_string_length - substring_length + 1):
        if substring_hash == current_slice_hash:
            if main_string[i:i+substring_length] == substring:
                return i
        if i < main_string_length - substring_length:
            current_slice_hash = (current_slice_hash - ord(main_string[i]) * h_multiplier) % modulus
            current_slice_hash = (current_slice_hash * base + ord(main_string[i + substring_length])) % modulus
            current_slice_hash = current_slice_hash % modulus
    return -1


# Читаємо вміст файлів
try:
    with open("стаття 1.txt", "r", encoding="utf-8") as file1, open("стаття 2.txt", "r", encoding="utf-8") as file2:
        article1 = file1.read()
        article2 = file2.read()
except UnicodeDecodeError:
    with open("стаття 1.txt", "r", encoding="windows-1251") as file1,  open("стаття 2.txt", "r", encoding="windows-1251") as file2:
        article1 = file1.read()
        article2 = file2.read()

# Вибір підрядків для пошуку
existing_substring = "алгоритм"  # Цей підрядок існує в тексті
nonexistent_substring = "абракадабра яку я сам придумав, бо не придумав нічого кращого"  # Цей підрядок не існує в тексті

# Вимірювання швидкості алгоритмів
def measure_performance(article, substring):
    bm_time = timeit.timeit(lambda: boyer_moore_search(article, substring), number=1)
    kmp_time = timeit.timeit(lambda: kmp_search(article, substring), number=1)
    rk_time = timeit.timeit(lambda: rabin_karp_search(article, substring), number=1)
    return bm_time, kmp_time, rk_time

performance_article1_existing = measure_performance(article1, existing_substring)
performance_article1_nonexistent = measure_performance(article1, nonexistent_substring)
performance_article2_existing = measure_performance(article2, existing_substring)
performance_article2_nonexistent = measure_performance(article2, nonexistent_substring)

print('performance_article1_existing (boyer_moore,kmp,rabin_karp)',performance_article1_existing)
print('performance_article1_nonexistent (boyer_moore,kmp,rabin_karp)',performance_article1_nonexistent) 
print('performance_article2_existing (boyer_moore,kmp,rabin_karp)',performance_article2_existing)
print('performance_article2_nonexistent (boyer_moore,kmp,rabin_karp)',performance_article1_nonexistent)

print(boyer_moore_search(article2, existing_substring))
print(boyer_moore_search(article2, nonexistent_substring))
