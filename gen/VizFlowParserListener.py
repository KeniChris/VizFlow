# Generated from VizFlowParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .VizFlowParser import VizFlowParser
else:
    from VizFlowParser import VizFlowParser

# This class defines a complete listener for a parse tree produced by VizFlowParser.
class VizFlowParserListener(ParseTreeListener):

    # Enter a parse tree produced by VizFlowParser#programa.
    def enterPrograma(self, ctx:VizFlowParser.ProgramaContext):
        pass

    # Exit a parse tree produced by VizFlowParser#programa.
    def exitPrograma(self, ctx:VizFlowParser.ProgramaContext):
        pass


    # Enter a parse tree produced by VizFlowParser#listaSentencias.
    def enterListaSentencias(self, ctx:VizFlowParser.ListaSentenciasContext):
        pass

    # Exit a parse tree produced by VizFlowParser#listaSentencias.
    def exitListaSentencias(self, ctx:VizFlowParser.ListaSentenciasContext):
        pass


    # Enter a parse tree produced by VizFlowParser#sentencia.
    def enterSentencia(self, ctx:VizFlowParser.SentenciaContext):
        pass

    # Exit a parse tree produced by VizFlowParser#sentencia.
    def exitSentencia(self, ctx:VizFlowParser.SentenciaContext):
        pass


    # Enter a parse tree produced by VizFlowParser#declaracionDataset.
    def enterDeclaracionDataset(self, ctx:VizFlowParser.DeclaracionDatasetContext):
        pass

    # Exit a parse tree produced by VizFlowParser#declaracionDataset.
    def exitDeclaracionDataset(self, ctx:VizFlowParser.DeclaracionDatasetContext):
        pass


    # Enter a parse tree produced by VizFlowParser#pipeline.
    def enterPipeline(self, ctx:VizFlowParser.PipelineContext):
        pass

    # Exit a parse tree produced by VizFlowParser#pipeline.
    def exitPipeline(self, ctx:VizFlowParser.PipelineContext):
        pass


    # Enter a parse tree produced by VizFlowParser#operacionesAdicionales.
    def enterOperacionesAdicionales(self, ctx:VizFlowParser.OperacionesAdicionalesContext):
        pass

    # Exit a parse tree produced by VizFlowParser#operacionesAdicionales.
    def exitOperacionesAdicionales(self, ctx:VizFlowParser.OperacionesAdicionalesContext):
        pass


    # Enter a parse tree produced by VizFlowParser#dashboardOpcional.
    def enterDashboardOpcional(self, ctx:VizFlowParser.DashboardOpcionalContext):
        pass

    # Exit a parse tree produced by VizFlowParser#dashboardOpcional.
    def exitDashboardOpcional(self, ctx:VizFlowParser.DashboardOpcionalContext):
        pass


    # Enter a parse tree produced by VizFlowParser#operacion.
    def enterOperacion(self, ctx:VizFlowParser.OperacionContext):
        pass

    # Exit a parse tree produced by VizFlowParser#operacion.
    def exitOperacion(self, ctx:VizFlowParser.OperacionContext):
        pass


    # Enter a parse tree produced by VizFlowParser#filterOp.
    def enterFilterOp(self, ctx:VizFlowParser.FilterOpContext):
        pass

    # Exit a parse tree produced by VizFlowParser#filterOp.
    def exitFilterOp(self, ctx:VizFlowParser.FilterOpContext):
        pass


    # Enter a parse tree produced by VizFlowParser#expresionLogica.
    def enterExpresionLogica(self, ctx:VizFlowParser.ExpresionLogicaContext):
        pass

    # Exit a parse tree produced by VizFlowParser#expresionLogica.
    def exitExpresionLogica(self, ctx:VizFlowParser.ExpresionLogicaContext):
        pass


    # Enter a parse tree produced by VizFlowParser#continuacionOr.
    def enterContinuacionOr(self, ctx:VizFlowParser.ContinuacionOrContext):
        pass

    # Exit a parse tree produced by VizFlowParser#continuacionOr.
    def exitContinuacionOr(self, ctx:VizFlowParser.ContinuacionOrContext):
        pass


    # Enter a parse tree produced by VizFlowParser#expresionAnd.
    def enterExpresionAnd(self, ctx:VizFlowParser.ExpresionAndContext):
        pass

    # Exit a parse tree produced by VizFlowParser#expresionAnd.
    def exitExpresionAnd(self, ctx:VizFlowParser.ExpresionAndContext):
        pass


    # Enter a parse tree produced by VizFlowParser#continuacionAnd.
    def enterContinuacionAnd(self, ctx:VizFlowParser.ContinuacionAndContext):
        pass

    # Exit a parse tree produced by VizFlowParser#continuacionAnd.
    def exitContinuacionAnd(self, ctx:VizFlowParser.ContinuacionAndContext):
        pass


    # Enter a parse tree produced by VizFlowParser#expresionNot.
    def enterExpresionNot(self, ctx:VizFlowParser.ExpresionNotContext):
        pass

    # Exit a parse tree produced by VizFlowParser#expresionNot.
    def exitExpresionNot(self, ctx:VizFlowParser.ExpresionNotContext):
        pass


    # Enter a parse tree produced by VizFlowParser#comparacion.
    def enterComparacion(self, ctx:VizFlowParser.ComparacionContext):
        pass

    # Exit a parse tree produced by VizFlowParser#comparacion.
    def exitComparacion(self, ctx:VizFlowParser.ComparacionContext):
        pass


    # Enter a parse tree produced by VizFlowParser#operadorRelacional.
    def enterOperadorRelacional(self, ctx:VizFlowParser.OperadorRelacionalContext):
        pass

    # Exit a parse tree produced by VizFlowParser#operadorRelacional.
    def exitOperadorRelacional(self, ctx:VizFlowParser.OperadorRelacionalContext):
        pass


    # Enter a parse tree produced by VizFlowParser#valor.
    def enterValor(self, ctx:VizFlowParser.ValorContext):
        pass

    # Exit a parse tree produced by VizFlowParser#valor.
    def exitValor(self, ctx:VizFlowParser.ValorContext):
        pass


    # Enter a parse tree produced by VizFlowParser#transformOp.
    def enterTransformOp(self, ctx:VizFlowParser.TransformOpContext):
        pass

    # Exit a parse tree produced by VizFlowParser#transformOp.
    def exitTransformOp(self, ctx:VizFlowParser.TransformOpContext):
        pass


    # Enter a parse tree produced by VizFlowParser#expresionAritmetica.
    def enterExpresionAritmetica(self, ctx:VizFlowParser.ExpresionAritmeticaContext):
        pass

    # Exit a parse tree produced by VizFlowParser#expresionAritmetica.
    def exitExpresionAritmetica(self, ctx:VizFlowParser.ExpresionAritmeticaContext):
        pass


    # Enter a parse tree produced by VizFlowParser#continuacionSuma.
    def enterContinuacionSuma(self, ctx:VizFlowParser.ContinuacionSumaContext):
        pass

    # Exit a parse tree produced by VizFlowParser#continuacionSuma.
    def exitContinuacionSuma(self, ctx:VizFlowParser.ContinuacionSumaContext):
        pass


    # Enter a parse tree produced by VizFlowParser#termino.
    def enterTermino(self, ctx:VizFlowParser.TerminoContext):
        pass

    # Exit a parse tree produced by VizFlowParser#termino.
    def exitTermino(self, ctx:VizFlowParser.TerminoContext):
        pass


    # Enter a parse tree produced by VizFlowParser#continuacionProducto.
    def enterContinuacionProducto(self, ctx:VizFlowParser.ContinuacionProductoContext):
        pass

    # Exit a parse tree produced by VizFlowParser#continuacionProducto.
    def exitContinuacionProducto(self, ctx:VizFlowParser.ContinuacionProductoContext):
        pass


    # Enter a parse tree produced by VizFlowParser#factor.
    def enterFactor(self, ctx:VizFlowParser.FactorContext):
        pass

    # Exit a parse tree produced by VizFlowParser#factor.
    def exitFactor(self, ctx:VizFlowParser.FactorContext):
        pass


    # Enter a parse tree produced by VizFlowParser#groupByOp.
    def enterGroupByOp(self, ctx:VizFlowParser.GroupByOpContext):
        pass

    # Exit a parse tree produced by VizFlowParser#groupByOp.
    def exitGroupByOp(self, ctx:VizFlowParser.GroupByOpContext):
        pass


    # Enter a parse tree produced by VizFlowParser#agregacion.
    def enterAgregacion(self, ctx:VizFlowParser.AgregacionContext):
        pass

    # Exit a parse tree produced by VizFlowParser#agregacion.
    def exitAgregacion(self, ctx:VizFlowParser.AgregacionContext):
        pass


    # Enter a parse tree produced by VizFlowParser#funcionAgregacion.
    def enterFuncionAgregacion(self, ctx:VizFlowParser.FuncionAgregacionContext):
        pass

    # Exit a parse tree produced by VizFlowParser#funcionAgregacion.
    def exitFuncionAgregacion(self, ctx:VizFlowParser.FuncionAgregacionContext):
        pass


    # Enter a parse tree produced by VizFlowParser#plotOp.
    def enterPlotOp(self, ctx:VizFlowParser.PlotOpContext):
        pass

    # Exit a parse tree produced by VizFlowParser#plotOp.
    def exitPlotOp(self, ctx:VizFlowParser.PlotOpContext):
        pass


    # Enter a parse tree produced by VizFlowParser#tipoGrafico.
    def enterTipoGrafico(self, ctx:VizFlowParser.TipoGraficoContext):
        pass

    # Exit a parse tree produced by VizFlowParser#tipoGrafico.
    def exitTipoGrafico(self, ctx:VizFlowParser.TipoGraficoContext):
        pass



del VizFlowParser