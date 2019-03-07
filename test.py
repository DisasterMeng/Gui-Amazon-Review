# from request import AmazonRequests
from dispose import AmazonDispose


def test():
    with open('amazon.txt', 'rb') as f:
        data = f.read()
        dispose = AmazonDispose(data)
        dispose.dispose()
    pass


if __name__ == '__main__':
    test()