SRC_DIR = src
SRC_FILES = $(shell find $(SRC_DIR) -name \*.py) main.py
BUILD_DIR = build
TARGET = $(BUILD_DIR)/function.zip

.PHONY: test
test:
	env PYTHONPATH=. pytest

.PHONY: clean
clean:
	find . -name \*.pyc -type f -delete
	find . -name __pycache__ -type d -delete
	rm -rf "$(BUILD_DIR)"

.PHONY: build
build: $(TARGET)
$(TARGET): $(SRC_DIR) $(SRC_FILES)
	mkdir -p build/
	zip "$(TARGET)" $(SRC_FILES)

.PHONY: deploy
deploy: $(TARGET)
	aws lambda update-function-code --region eu-west-1 --function-name "lunchRota" --zip-file "fileb://$(TARGET)" --query "LastModified"
	aws lambda update-function-configuration --region eu-west-1 --function-name "lunchRota" --handler "main.lambda_handler" --query "Handler"
