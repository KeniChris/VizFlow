# Generated from VizFlowParser.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .VizFlowParser import VizFlowParser
else:
    from VizFlowParser import VizFlowParser

# This class defines a complete generic visitor for a parse tree produced by VizFlowParser.

class VizFlowParserVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by VizFlowParser#programa.
    def visitPrograma(self, ctx:VizFlowParser.ProgramaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#sentencia.
    def visitSentencia(self, ctx:VizFlowParser.SentenciaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#declaracionDataset.
    def visitDeclaracionDataset(self, ctx:VizFlowParser.DeclaracionDatasetContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#pipeline.
    def visitPipeline(self, ctx:VizFlowParser.PipelineContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#operacion.
    def visitOperacion(self, ctx:VizFlowParser.OperacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#filterOp.
    def visitFilterOp(self, ctx:VizFlowParser.FilterOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#expresionLogica.
    def visitExpresionLogica(self, ctx:VizFlowParser.ExpresionLogicaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#expresionAnd.
    def visitExpresionAnd(self, ctx:VizFlowParser.ExpresionAndContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#expresionNot.
    def visitExpresionNot(self, ctx:VizFlowParser.ExpresionNotContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#comparacion.
    def visitComparacion(self, ctx:VizFlowParser.ComparacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#operadorRelacional.
    def visitOperadorRelacional(self, ctx:VizFlowParser.OperadorRelacionalContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#valor.
    def visitValor(self, ctx:VizFlowParser.ValorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#transformOp.
    def visitTransformOp(self, ctx:VizFlowParser.TransformOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#expresionAritmetica.
    def visitExpresionAritmetica(self, ctx:VizFlowParser.ExpresionAritmeticaContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#termino.
    def visitTermino(self, ctx:VizFlowParser.TerminoContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#factor.
    def visitFactor(self, ctx:VizFlowParser.FactorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#groupByOp.
    def visitGroupByOp(self, ctx:VizFlowParser.GroupByOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#agregacion.
    def visitAgregacion(self, ctx:VizFlowParser.AgregacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#funcionAgregacion.
    def visitFuncionAgregacion(self, ctx:VizFlowParser.FuncionAgregacionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#plotOp.
    def visitPlotOp(self, ctx:VizFlowParser.PlotOpContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by VizFlowParser#tipoGrafico.
    def visitTipoGrafico(self, ctx:VizFlowParser.TipoGraficoContext):
        return self.visitChildren(ctx)



del VizFlowParser