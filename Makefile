BUILD_DIR = ./build
SRC_DIR = ./src
DATA_DIR = ./data

PY = /usr/bin/python3

.PHONY: all
all: setup run

$(BUILD_DIR)/speedtest:
	$(SRC_DIR)/setup.sh $(BUILD_DIR)

.PHONY: build
build: $(BUILD_DIR)/speedtest

.PHONY: run
run: build
	$(PY) $(SRC_DIR)/main.py $(BUILD_DIR)/speedtest $(DATA_DIR)

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(DATA_DIR)