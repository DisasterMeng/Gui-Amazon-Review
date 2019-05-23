from dispose import AmazonDispose
from request import AmazonRequests


def test():
    with open('amazon.txt', 'rb') as f:
        data = f.read()
        dispose = AmazonDispose(data, 'US', 'B076MP43X5')
        print(dispose.dispose())
    # request = AmazonRequests('US', 'B01N2K4U7')
    # print(request.getAmaoznData())
    pass


if __name__ == '__main__':
    test()
