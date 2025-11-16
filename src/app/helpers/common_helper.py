from faker import Faker


fake = Faker(locale='en')


def get_random_number(number_digits: int = 2) -> int:
    return fake.random_number(
        digits=number_digits,
        fix_len=True,
    )


def get_random_email() -> str:
    return fake.email()


def get_random_first_name() -> str:
    return fake.first_name()


def get_random_last_name() -> str:
    return fake.last_name()


def get_random_url() -> str:
    return fake.url()


if __name__ == '__main__':
    print(f"{get_random_number(number_digits=5)}")