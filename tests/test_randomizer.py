import numpy as np
import pytest
from core.utils import Randomizer
from core.models.config_models import IntConfig, FloatConfig, StringConfig

value_size = 5
value_min = 1
value_max = 11
float_round = 5
str_length = 5
str_type = "mixed"

@pytest.fixture
def randomizer():
    rng = Randomizer(42)
    return {
        "random_int": rng.get_random_int,
        "random_float": rng.get_random_float,
        "random_string": rng.get_random_string
    }

@pytest.fixture
def configs():
    int_config = IntConfig(size=value_size, int_min=value_min, int_max=value_max)
    float_config = FloatConfig(size=value_size, float_min=value_min, float_max=value_max, float_round=float_round)
    string_config = StringConfig(size=value_size, string_length=str_length, string_type=str_type)
    
    scalar_int_config = IntConfig(size=1, int_min=value_min, int_max=value_max)
    scalar_float_config = FloatConfig(size=1, float_min=value_min, float_max=value_max, float_round=float_round)
    scalar_string_config = StringConfig(size=1, string_length=str_length, string_type=str_type)
    
    return {
        "int_config": int_config,
        "float_config": float_config,
        "string_config": string_config,
        
        "scalar_int_config": scalar_int_config,
        "scalar_float_config": scalar_float_config,
        "scalar_string_config": scalar_string_config
    }
    
def test_random_reproducibility(configs):
    rng1 = Randomizer(42)
    rng2 = Randomizer(42)
    
    for _ in range(5):
        values1 = rng1.get_random_int(configs.get("int_config"))
        values2 = rng2.get_random_int(configs.get("int_config"))
        assert np.array_equal(values1, values2)
        
        values3 = rng1.get_random_float(configs.get("float_config"))
        values4 = rng2.get_random_float(configs.get("float_config"))
        assert np.array_equal(values3, values4)
        
        values5 = rng1.get_random_string(configs.get("string_config"))
        values6 = rng2.get_random_string(configs.get("string_config"))
        assert values5 == values6
        
def test_random_type(randomizer, configs):
    random_int = randomizer.get("random_int")(configs.get("int_config"))
    random_float = randomizer.get("random_float")(configs.get("float_config"))
    random_string = randomizer.get("random_string")(configs.get("string_config"))
    
    assert isinstance(random_int, np.ndarray)
    assert isinstance(random_float, np.ndarray)
    assert isinstance(random_string, list)
    
def test_random_scalar_type(randomizer, configs):
    random_int = randomizer.get("random_int")(configs.get("scalar_int_config"))
    random_float = randomizer.get("random_float")(configs.get("scalar_float_config"))
    random_string = randomizer.get("random_string")(configs.get("scalar_string_config"))
    
    assert isinstance(random_int, int)
    assert isinstance(random_float, float)
    assert isinstance(random_string, str)
    
def test_random_size(randomizer, configs):
    random_int = randomizer.get("random_int")(configs.get("int_config"))
    random_float = randomizer.get("random_float")(configs.get("float_config"))
    random_string = randomizer.get("random_string")(configs.get("string_config"))
    
    assert random_int.size == value_size
    assert random_float.size == value_size
    assert len(random_string) == value_size
    
    #min value include, max value exclude
def test_random_values_range(randomizer, configs):
    for _ in range(10):
        random_int = randomizer.get("random_int")(configs.get("int_config"))
        random_float = randomizer.get("random_float")(configs.get("float_config"))

        assert np.all(random_int >= value_min)
        assert np.all(random_int < value_max)
        assert np.all(random_float >= value_min)
        assert np.all(random_float < value_max)
        
def test_string_length(randomizer, configs):
    random_string = randomizer.get("random_string")(configs.get("string_config"))
    for value in random_string:
        assert len(value) == str_length
        
def test_float_round(randomizer, configs):
    random_float = randomizer.get("random_float")(configs.get("float_config"))
    for value in random_float:
        decimal_point = str(value).split(".")[1]
        assert len(decimal_point) == float_round