from core.utils import Helper

def test_get_dict_length_logic():
    example_data = {"name": {
        "rifki": {
            "age": 99,
            "id": 250301123,
            "hobby": {
                "at_home": "game",
                "at_work": {
                    "on_break": "scroll_socmed"
                }
            }
        },
        "nafis": {
            "age": 99,
            "id": 250301123,
            "hobby": "overthinking"
        }}}
    dict_depth = Helper.get_dict_depth(example_data)
    assert dict_depth == 5
    