#!/bin/bash

echo "▶️ Formatting code with black (max line = 150)..."
black app test

echo "▶️ Sorting imports with isort (line length = 150)..."
isort app test

echo "▶️ Checking code with flake8 (max line = 150)..."
flake8 app test

echo "✅ Formatting and linting complete."
