import numpy as np
import pytest
from core.utils import Randomizer
from core.models.config_models import IntConfig, FloatConfig, StringConfig

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
    int_config = IntConfig(size=5, int_min=1, int_max=11)
    float_config = FloatConfig(size=5, float_min=1, float_max=11, float_round=5)
    string_config = StringConfig(size=5, string_length=5, string_type="mixed")
    
    scalar_int_config = IntConfig(size=1, int_min=1, int_max=11)
    scalar_float_config = FloatConfig(size=1, float_min=1, float_max=11, float_round=5)
    scalar_string_config = StringConfig(size=1, string_length=5, string_type="mixed")
    
    return {
        "int_config": int_config,
        "float_config": float_config,
        "string_config": string_config,
        
        "scalar_int_config": scalar_int_config,
        "scalar_float_config": scalar_float_config,
        "scalar_string_config": scalar_string_config
    }
    
def test_random_values(randomizer, configs):    
    int_expected = np.array([1, 8, 7, 5, 5])
    int_result = randomizer.get("random_int")(configs.get("int_config"))
    
    float_expected = np.array([7.97368, 1.94177, 10.75622, 8.6114, 8.86064])
    float_result = randomizer.get("random_float")(configs.get("float_config"))
    
    string_expected = []
    string_result = randomizer.get("random_string")(configs.get("string_config"))
    
    assert np.array_equal(int_expected, int_result)
    assert np.array_equal(float_expected, float_result)
    assert string_expected == string_result