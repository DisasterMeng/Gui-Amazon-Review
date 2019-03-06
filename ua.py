import random


def get_random_ua():
    with open('ua.txt', encoding='utf-8') as file:
        lines = file.readlines()

        index = random.randint(0, len(lines))
        return lines[index]


if __name__ == '__main__':
    ua = get_random_ua()
    print(ua)
