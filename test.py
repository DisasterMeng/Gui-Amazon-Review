from dispose import AmazonDispose


def test():
    with open('amazon.txt', 'rb') as f:
        data = f.read()
        dispose = AmazonDispose(data, 'B076MP43X5', 'US')
        print(dispose.isNextPage())
    pass


if __name__ == '__main__':
    test()