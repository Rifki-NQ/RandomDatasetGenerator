from core.utils import Randomizer
from core.config_models import IntConfig, FloatConfig, StringConfig

def test_randomizer():
    create_random = Randomizer()
    print(create_random.get_random_int(IntConfig(10, 1, 10)))
    print(create_random.get_random_float(FloatConfig(10, 1, 10, 2)))
    print(create_random.get_random_string(StringConfig(10, 3, "mixed")))
    print(create_random.get_random_mixed(10))