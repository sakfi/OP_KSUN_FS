import yaml

try:
    with open('.github/actions/action.yml', 'r', encoding='utf-8') as f:
        yaml.safe_load(f)
    print("YAML parses OK")
except Exception as e:
    print(e)
