import os

APP_DIR = "app"
TEST_DIR = "test"

EXCLUDE_FILES = {"__init__.py", "main.py"}
TEST_TEMPLATE = """# Auto-generated test for {module_path}

def test_placeholder():
    assert True
"""

def ensure_test_file(app_path: str, test_path: str):
    with open(test_path, "w") as f:
        rel_module = app_path.replace("/", ".").replace(".py", "")
        f.write(TEST_TEMPLATE.format(module_path=rel_module))
        print(f"✅ Created: {test_path}")

def main():
    for dirpath, _, filenames in os.walk(APP_DIR):
        for filename in filenames:
            if filename.endswith(".py") and filename not in EXCLUDE_FILES:
                app_file_path = os.path.join(dirpath, filename)

                # Convert to relative path
                rel_path = os.path.relpath(app_file_path, APP_DIR)

                # Create equivalent test path
                test_file_name = f"test_{filename}"
                test_rel_path = os.path.join(TEST_DIR, os.path.dirname(rel_path), test_file_name)

                # Ensure directory exists
                os.makedirs(os.path.dirname(test_rel_path), exist_ok=True)

                # Only create if not already exists
                if not os.path.exists(test_rel_path):
                    ensure_test_file(app_file_path, test_rel_path)

if __name__ == "__main__":
    main()
