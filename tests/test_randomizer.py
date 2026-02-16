from core.generator.generator_logic import Randomizer

def test_randomizer():
    create_random = Randomizer()
    print(create_random.get_random_int(10, 1, 10))
    print(create_random.get_random_float(20, 1, 10, 2))
    print(create_random.get_random_string(10, 3, "mixed"))