# Sum homogenous numbers
def T(n):
    t_sum = 0
    for num in range(0, 10**n):
        digits = [int(i) for i in str(num)]
        mid = len(digits) // 2
        if len(digits) % 2 == 0:
            left = sum(digits[:mid])
        else:
            left = sum(digits[:mid + 1])
        right = sum(digits[mid:])

        if left == right:
            t_sum += num
    return t_sum


if __name__ == '__main__':
    n = int(input())
    result = T(n)
    print(result)
