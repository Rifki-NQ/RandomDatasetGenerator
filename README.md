# RandomDatasetGenerator
A CLI-based app used to generate random dataset in CSV file with customizable randomness configuration

## Features
1. Generator
    - Generate random dataset
    - Generate custom random dataset

2. Setting
    - Show current filepaths
    - Change filepath for generated dataset
    - Show random value configuration
    - Change random value configuration
    - Update all random value configuration

## Requirements
- Python 3.10+
- Libraries listed in 'requirements.txt'

## Installation
1. Clone the repository: `git clone https://github.com/Rifki-NQ/RandomDatasetGenerator`
2. Navigate into the project directory: `cd RandomDatasetGenerator`
3. Install dependencies: `pip install -r requirements.txt`

## Usage
```bash
python main.py
```

## TODO
- add one central layer for config data validation
- use dict instead of list for method for change_random_config and update_random_configs
- add argsparse for easier use