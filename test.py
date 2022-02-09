def g(n):
    for i in range(n):
        yield i
        yield i * 10


if __name__ == "__main__":
    a = g(10)
    while next(a):
        print(next(a))
