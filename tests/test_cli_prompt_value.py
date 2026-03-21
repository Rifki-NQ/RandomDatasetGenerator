from core.generator.generator_setting_cli import _BaseCLI
cli = _BaseCLI()
input_message =  "Enter value: "

#test cases for generator_setting_cli _prompt_value returned value type

# -------------- test cases with positive values --------------

#accepted type = int
def test_prompt_value_input_int(monkeypatch):
    input_values = iter(["word_1", "word_2", "20.5", "50"]) 
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("int", input_message)
    assert value == 50
    assert isinstance(value, int)

#accepted type = int or float
def test_prompt_value_numbers_input_int(monkeypatch):
    input_values = iter(["word_1", "word_2", "20", "20.5"]) # int number come first
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("numbers", input_message)
    assert value == 20
    assert isinstance(value, int)

#accepted type = int or float
def test_prompt_value_numbers_input_float(monkeypatch):
    input_values = iter(["word_1", "word_2", "20.5", "20"]) # float number come first
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("numbers", input_message)
    assert value == 20.5
    assert isinstance(value, float)
    
# -------------- test cases with minus values --------------

#accepted type = int
def test_prompt_value_input_minus_int(monkeypatch):
    input_values = iter(["word_1", "word_2", "-20.5", "-50"]) 
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("int", input_message)
    assert value == -50
    assert isinstance(value, int)

#accepted type = int or float
def test_prompt_value_numbers_input_minus_int(monkeypatch):
    input_values = iter(["word_1", "word_2", "-20", "-20.5"]) # int number come first
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("numbers", input_message)
    assert value == -20
    assert isinstance(value, int)

#accepted type = int or float
def test_prompt_value_numbers_input_minus_float(monkeypatch):
    input_values = iter(["word_1", "word_2", "-20.5", "-20"]) # float number come first
    monkeypatch.setattr("builtins.input", lambda *args: next(input_values))
    value = cli._prompt_value("numbers", input_message)
    assert value == -20.5
    assert isinstance(value, float)