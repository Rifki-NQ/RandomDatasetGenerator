from core.utils import Randomizer

def test_randomizer():
    create_random = Randomizer()
    print(create_random.get_random_int(1, 1, 10))
    print(create_random.get_random_float(1, 1, 10, 2))
    print(create_random.get_random_string(1, 3, "mixed"))