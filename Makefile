LEXER = VizFlowLexer.g4
PARSER = VizFlowParser.g4
OUTPUT_DIR = gen
JAR_PROJECT = $(CURDIR)/tools/antlr-4.13.1-complete.jar

JAR_LOCAL  = $(HOME)/.local/lib/antlr-4.13.1-complete.jar
JAR_SYSTEM = /usr/local/lib/antlr-4.13.1-complete.jar

all:
	@mkdir -p $(OUTPUT_DIR)
	@if [ -f "$(JAR_PROJECT)" ]; then \
		java -jar "$(JAR_PROJECT)" -Dlanguage=Python3 -visitor $(LEXER) -o $(OUTPUT_DIR); \
		java -jar "$(JAR_PROJECT)" -Dlanguage=Python3 -visitor $(PARSER) -lib $(OUTPUT_DIR) -o $(OUTPUT_DIR); \
	elif [ -f "$(JAR_LOCAL)" ]; then \
		java -jar "$(JAR_LOCAL)" -Dlanguage=Python3 -visitor $(LEXER) -o $(OUTPUT_DIR); \
		java -jar "$(JAR_LOCAL)" -Dlanguage=Python3 -visitor $(PARSER) -lib $(OUTPUT_DIR) -o $(OUTPUT_DIR); \
	elif [ -f "$(JAR_SYSTEM)" ]; then \
		java -jar "$(JAR_SYSTEM)" -Dlanguage=Python3 -visitor $(LEXER) -o $(OUTPUT_DIR); \
		java -jar "$(JAR_SYSTEM)" -Dlanguage=Python3 -visitor $(PARSER) -lib $(OUTPUT_DIR) -o $(OUTPUT_DIR); \
	elif command -v antlr4 > /dev/null 2>&1; then \
		antlr4 -Dlanguage=Python3 -visitor $(LEXER) -o $(OUTPUT_DIR); \
		antlr4 -Dlanguage=Python3 -visitor $(PARSER) -lib $(OUTPUT_DIR) -o $(OUTPUT_DIR); \
	else \
		echo "Error: No se encontró ANTLR4. Verifique la instalación del .jar o antlr4."; exit 1; \
	fi
	@echo "Generación léxica y sintáctica de VizFlow completada exitosamente en $(OUTPUT_DIR)/."

clean:
	rm -f $(OUTPUT_DIR)/VizFlowLexer*.py
	rm -f $(OUTPUT_DIR)/VizFlowLexer*.tokens
	rm -f $(OUTPUT_DIR)/VizFlowLexer*.interp
	rm -f $(OUTPUT_DIR)/VizFlowParser*.py
	rm -f $(OUTPUT_DIR)/VizFlowParser*.tokens
	rm -f $(OUTPUT_DIR)/VizFlowParser*.interp
	rm -rf __pycache__ $(OUTPUT_DIR)/__pycache__ tests/__pycache__
	@echo "Archivos generados eliminados."
