BUILD_DIR = ./build
SRC_DIR = ./src
DATA_DIR = ./data

PY = /usr/bin/python

.PHONY: all
all: setup run

$(BUILD_DIR)/speedtest:
	$(SRC_DIR)/setup.sh $(BUILD_DIR)

.PHONY: run
run: $(BUILD_DIR)/speedtest
	$(PY) $(SRC_DIR)/network_monitor.py $(BUILD_DIR)/speedtest $(DATA_DIR)

.PHONY: clean
clean:
	rm -rf $(BUILD_DIR)
	rm -rf $(DATA_DIR)