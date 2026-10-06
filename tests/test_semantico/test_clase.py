"""Validación de ámbitos e inicialización del enfoque de Semana 6."""

import shutil
import tempfile
import unittest
from pathlib import Path
from antlr4 import CommonTokenStream, InputStream
from gen.VizFlowLexer import VizFlowLexer
from gen.VizFlowParser import VizFlowParser
from vizflow.errors import SemanticError
from vizflow.frontend import analyze_source
from vizflow.semantic import AnalysisResult
from vizflow.semantic_visitor import SemanticVisitor
from vizflow.symbols import NUMBER, STRING, SymbolTable

PROJECT = Path(__file__).resolve().parents[2]


class SymbolTableTests(unittest.TestCase):
    def test_declaracion_por_ambito_y_flags_del_ejemplo(self):
        table = SymbolTable()
        symbol = table.declare("monto", NUMBER, 4)
        self.assertIs(table.scopes["global"]["monto"], symbol)
        self.assertEqual((symbol.name, symbol.type_, symbol.scope, symbol.line),
                         ("monto", NUMBER, "global", 4))
        self.assertFalse(symbol.initialized)
        self.assertFalse(symbol.used)
        with self.assertRaises(SemanticError) as context:
            table.declare("monto", STRING, 5)
        self.assertEqual(context.exception.code, "SEM002")
        self.assertEqual(context.exception.line, 5)
        self.assertIs(table.lookup("monto"), symbol)

    def test_busqueda_respeta_sombra_y_restauracion_del_ambito(self):
        table = SymbolTable()
        global_symbol = table.declare("valor", NUMBER, 1)
        table.enter_scope("pipeline_1_L3")
        local_symbol = table.declare("valor", STRING, 3)
        self.assertIs(table.lookup("valor"), local_symbol)
        table.enter_scope("interno")
        self.assertIs(table.lookup("valor"), local_symbol)
        table.exit_scope()
        table.exit_scope()
        self.assertIs(table.lookup("valor"), global_symbol)
        self.assertIsNone(table.lookup("desconocido"))
        with self.assertRaises(RuntimeError):
            table.exit_scope()
        self.assertEqual(table.current_scope, "global")

    def test_advertencias_respetan_el_flag_used(self):
        table = SymbolTable()
        used = table.declare("usado", NUMBER, 1)
        table.declare("sin_uso", STRING, 2)
        used.used = True
        warnings = table.unused_warnings()
        self.assertEqual(len(warnings), 1)
        self.assertIn("'sin_uso'", warnings[0])


class ClassroomVisitorTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        shutil.copy2(PROJECT / "data/ventas.csv", self.root / "ventas.csv")
        self.prefix = 'DATASET ventas = LOAD "ventas.csv";\n\n'

    def tearDown(self):
        self.temp.cleanup()

    def analyze(self, body: str) -> AnalysisResult:
        result = analyze_source(self.prefix + body, self.root)
        self.assertIsNotNone(result.analysis)
        assert result.analysis is not None
        return result.analysis

    def test_tuberia_registra_flags_y_no_modifica_simbolos_globales(self):
        result = self.analyze("ventas |> TRANSFORM(total = monto * 2) "
                              "|> FILTER(total > 10);")
        self.assertTrue(result.ok, result.diagnostics)
        table = result.symbols
        dataset = table.datasets["ventas"]
        assert dataset.columns is not None
        local = table.scopes["pipeline_1_L3"]
        self.assertTrue(dataset.initialized)
        self.assertTrue(dataset.used)
        self.assertTrue(local["monto"].used)
        self.assertTrue(local["total"].initialized)
        self.assertTrue(local["total"].used)
        self.assertEqual(local["total"].type_, NUMBER)
        self.assertEqual(local["total"].scope, "pipeline_1_L3")
        self.assertFalse(dataset.columns["monto"].used)
        self.assertNotIn("total", dataset.columns)
        self.assertEqual(table.current_scope, "global")

    def test_transform_fallido_no_inicializa_un_destino_nuevo(self):
        result = self.analyze("ventas |> TRANSFORM(total = categoria + 1) "
                              "|> FILTER(total > 10);")
        self.assertEqual([d.code for d in result.diagnostics], ["SEM004", "SEM003"])
        local = result.symbols.scopes["pipeline_1_L3"]
        self.assertNotIn("total", local)

    def test_transform_fallido_conserva_un_destino_previo(self):
        result = self.analyze("ventas |> TRANSFORM(monto = categoria + 1) "
                              "|> FILTER(monto > 10);")
        self.assertEqual([d.code for d in result.diagnostics], ["SEM004"])
        symbol = result.pipelines[0].columns["monto"]
        self.assertTrue(symbol.initialized)
        self.assertEqual(symbol.datatype, NUMBER)

    def test_columnas_locales_no_se_filtran_a_otra_tuberia(self):
        result = self.analyze("ventas |> TRANSFORM(total = monto * 2);\n"
                              "ventas |> FILTER(total > 10);")
        self.assertEqual([d.code for d in result.diagnostics], ["SEM003"])
        table = result.symbols
        self.assertIn("total", table.scopes["pipeline_1_L3"])
        self.assertNotIn("total", table.scopes["pipeline_2_L4"])
        self.assertIsNone(table.lookup("total"))
        self.assertEqual(table.current_scope, "global")

    def test_load_fallido_no_marca_dataset_como_inicializado(self):
        result = analyze_source('DATASET ventas = LOAD "inexistente.csv";', self.root)
        self.assertEqual([d.code for d in result.diagnostics], ["SEM011"])
        assert result.analysis is not None
        self.assertFalse(result.analysis.symbols.datasets["ventas"].initialized)

    def test_null_no_es_una_variable_sin_inicializar(self):
        (self.root / "vacios.csv").write_text("monto\n\"\"\n", encoding="utf-8")
        result = analyze_source('DATASET ventas = LOAD "vacios.csv";\n'
                                'ventas |> FILTER(monto == NULL);', self.root)
        self.assertTrue(result.ok, result.diagnostics)
        assert result.analysis is not None
        symbol = result.analysis.pipelines[0].columns["monto"]
        self.assertTrue(symbol.initialized)
        self.assertTrue(symbol.nullable)

    def test_visitor_acumula_errores_y_se_reinicia_entre_programas(self):
        def parse(source):
            parser = VizFlowParser(CommonTokenStream(VizFlowLexer(InputStream(source))))
            tree = parser.programa()
            self.assertEqual(parser.getNumberOfSyntaxErrors(), 0)
            return tree

        visitor = SemanticVisitor(self.root)
        rejected = visitor.visit(parse('fantasma |> FILTER(monto > 10);'))
        self.assertFalse(rejected.ok)
        self.assertIsInstance(visitor.errors[0], SemanticError)
        self.assertEqual(visitor.errors[0].code, "SEM001")
        accepted = visitor.visit(parse(self.prefix + 'ventas |> FILTER(monto > 10);'))
        self.assertTrue(accepted.ok, accepted.diagnostics)
        self.assertEqual(visitor.errors, [])
        self.assertEqual(set(visitor.symtab.datasets), {"ventas"})


if __name__ == "__main__":
    unittest.main()
