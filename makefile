CXX = g++

CXXFLAGS = -std=c++17 -Wall -g -Iinclude

# Directories
SRC_DIR = src
BIN_DIR = bin

TARGET = $(BIN_DIR)/program.exe

# Find .cpp files in SRC_DIR
SOURCES = $(wildcard $(SRC_DIR)/*.cpp $(SRC_DIR)/*/*.cpp)

# Names for object files
OBJECTS = $(patsubst $(SRC_DIR)/%.cpp,$(BIN_DIR)/%.o,$(SOURCES))

all: $(BIN_DIR) $(TARGET)

# Bin directory
$(BIN_DIR):
	@mkdir -p $(BIN_DIR)

# Rules for build
$(TARGET): $(OBJECTS)
	@echo "Linking..."
	$(CXX) $(OBJECTS) -o $(TARGET)

# Rule for compiling .cpp into .o
$(BIN_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "Compiling $<..."
	@mkdir -p $(dir $@)
	$(CXX) $(CXXFLAGS) -c $< -o $@


run: all
	@echo "Running executable..."
	./$(TARGET)

clean:
	@echo "Cleaning project..."
	rm -rf $(BIN_DIR)

.PHONY: all clean run