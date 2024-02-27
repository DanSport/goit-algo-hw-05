def bound(arr, value):
    left, right = 0, len(arr) - 1
    iterations = 0
    while left <= right:
        iterations += 1
        mid = left + (right - left) // 2
        if arr[mid] == value:
            return (iterations, arr[mid])
        elif arr[mid] < value:
            left = mid + 1
        else:
            right = mid - 1
    
    if left >= len(arr):
        # Тут повертаємо None або інше спеціальне значення, якщо в масиві немає елемента більшого за value
        return (iterations, None)
    else:
        # Якщо ж left в межах масиву, це буде наша "верхня межа"
        return (iterations, arr[left])

# Тестуємо нашу функцію
arr = [1.1, 1.3, 2.5, 3.8, 4.6, 5.9]
print(bound(arr, 3.5))  # Має вивести: (кількість ітерацій, 3.8)
print(bound(arr, 5.8))  # Має вивести: (кількість ітерацій, 5.9)
print(bound(arr, 6.0))  # Має вивести: (кількість ітерацій, None), оскільки 6.0 більше за будь-який елемент в масиві
