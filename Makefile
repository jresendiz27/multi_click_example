build_pyinstaller:
	poetry run pyinstaller --specpath ./ ./multi_click_example/main.py  --clean -n multi_click_example_${TARGET_OS} -F
test:
	poetry run pytest
upload:
	./scripts/upload_package.sh
