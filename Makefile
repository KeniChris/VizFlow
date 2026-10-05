FILENAME = VizFlowLexer.g4
PREFIX = $(basename $(FILENAME))
OUTPUT_DIR = gen

# Rutas estándar del jar de ANTLR4
JAR_LOCAL  = $(HOME)/.local/lib/antlr-4.13.1-complete.jar
JAR_SYSTEM = /usr/local/lib/antlr-4.13.1-complete.jar

all:
	@mkdir -p $(OUTPUT_DIR)
	@if [ -f "$(JAR_LOCAL)" ]; then \
		java -jar $(JAR_LOCAL) -Dlanguage=Python3 $(FILENAME) -o $(OUTPUT_DIR); \
	elif [ -f "$(JAR_SYSTEM)" ]; then \
		java -jar $(JAR_SYSTEM) -Dlanguage=Python3 $(FILENAME) -o $(OUTPUT_DIR); \
	elif command -v antlr4 > /dev/null 2>&1; then \
		antlr4 -Dlanguage=Python3 $(FILENAME) -o $(OUTPUT_DIR); \
	else \
		echo "Error: No se encontró ANTLR4. Verifique la instalación del .jar o antlr4."; exit 1; \
	fi
	@echo "Generación léxica de $(PREFIX) completada exitosamente en $(OUTPUT_DIR)/."

clean:
	rm -f $(OUTPUT_DIR)/$(PREFIX)*.py
	rm -f $(OUTPUT_DIR)/$(PREFIX)*.tokens
	rm -f $(OUTPUT_DIR)/$(PREFIX)*.interp
	rm -rf __pycache__ $(OUTPUT_DIR)/__pycache__ tests/__pycache__
	@echo "Archivos generados eliminados."
