# Generated from VizFlowParser.g4 by ANTLR 4.13.1
# encoding: utf-8
from antlr4 import *
from io import StringIO
import sys
if sys.version_info[1] > 5:
	from typing import TextIO
else:
	from typing.io import TextIO

def serializedATN():
    return [
        4,1,47,186,2,0,7,0,2,1,7,1,2,2,7,2,2,3,7,3,2,4,7,4,2,5,7,5,2,6,7,
        6,2,7,7,7,2,8,7,8,2,9,7,9,2,10,7,10,2,11,7,11,2,12,7,12,2,13,7,13,
        2,14,7,14,2,15,7,15,2,16,7,16,2,17,7,17,2,18,7,18,2,19,7,19,2,20,
        7,20,1,0,4,0,44,8,0,11,0,12,0,45,1,0,1,0,1,1,1,1,3,1,52,8,1,1,2,
        1,2,1,2,1,2,1,2,1,2,1,2,1,3,1,3,1,3,1,3,1,3,5,3,66,8,3,10,3,12,3,
        69,9,3,1,3,1,3,3,3,73,8,3,1,3,1,3,1,4,1,4,1,4,1,4,3,4,81,8,4,1,5,
        1,5,1,5,1,5,1,5,1,6,1,6,1,6,5,6,91,8,6,10,6,12,6,94,9,6,1,7,1,7,
        1,7,5,7,99,8,7,10,7,12,7,102,9,7,1,8,1,8,1,8,1,8,1,8,1,8,1,8,3,8,
        111,8,8,1,9,1,9,1,9,1,9,1,10,1,10,1,11,1,11,1,12,1,12,1,12,1,12,
        1,12,1,12,1,12,1,13,1,13,1,13,5,13,131,8,13,10,13,12,13,134,9,13,
        1,14,1,14,1,14,5,14,139,8,14,10,14,12,14,142,9,14,1,15,1,15,1,15,
        1,15,1,15,1,15,1,15,3,15,151,8,15,1,16,1,16,1,16,1,16,1,16,1,16,
        1,16,1,17,1,17,1,17,1,17,1,17,1,17,1,17,1,17,3,17,168,8,17,1,18,
        1,18,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,1,19,
        1,20,1,20,1,20,0,0,21,0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,
        32,34,36,38,40,0,6,1,0,25,30,2,0,18,20,40,43,1,0,32,33,1,0,34,35,
        1,0,8,11,1,0,13,15,181,0,43,1,0,0,0,2,51,1,0,0,0,4,53,1,0,0,0,6,
        60,1,0,0,0,8,80,1,0,0,0,10,82,1,0,0,0,12,87,1,0,0,0,14,95,1,0,0,
        0,16,110,1,0,0,0,18,112,1,0,0,0,20,116,1,0,0,0,22,118,1,0,0,0,24,
        120,1,0,0,0,26,127,1,0,0,0,28,135,1,0,0,0,30,150,1,0,0,0,32,152,
        1,0,0,0,34,167,1,0,0,0,36,169,1,0,0,0,38,171,1,0,0,0,40,183,1,0,
        0,0,42,44,3,2,1,0,43,42,1,0,0,0,44,45,1,0,0,0,45,43,1,0,0,0,45,46,
        1,0,0,0,46,47,1,0,0,0,47,48,5,0,0,1,48,1,1,0,0,0,49,52,3,4,2,0,50,
        52,3,6,3,0,51,49,1,0,0,0,51,50,1,0,0,0,52,3,1,0,0,0,53,54,5,1,0,
        0,54,55,5,43,0,0,55,56,5,31,0,0,56,57,5,2,0,0,57,58,5,40,0,0,58,
        59,5,39,0,0,59,5,1,0,0,0,60,61,5,43,0,0,61,62,5,24,0,0,62,67,3,8,
        4,0,63,64,5,24,0,0,64,66,3,8,4,0,65,63,1,0,0,0,66,69,1,0,0,0,67,
        65,1,0,0,0,67,68,1,0,0,0,68,72,1,0,0,0,69,67,1,0,0,0,70,71,5,24,
        0,0,71,73,5,7,0,0,72,70,1,0,0,0,72,73,1,0,0,0,73,74,1,0,0,0,74,75,
        5,39,0,0,75,7,1,0,0,0,76,81,3,10,5,0,77,81,3,24,12,0,78,81,3,32,
        16,0,79,81,3,38,19,0,80,76,1,0,0,0,80,77,1,0,0,0,80,78,1,0,0,0,80,
        79,1,0,0,0,81,9,1,0,0,0,82,83,5,3,0,0,83,84,5,36,0,0,84,85,3,12,
        6,0,85,86,5,37,0,0,86,11,1,0,0,0,87,92,3,14,7,0,88,89,5,22,0,0,89,
        91,3,14,7,0,90,88,1,0,0,0,91,94,1,0,0,0,92,90,1,0,0,0,92,93,1,0,
        0,0,93,13,1,0,0,0,94,92,1,0,0,0,95,100,3,16,8,0,96,97,5,21,0,0,97,
        99,3,16,8,0,98,96,1,0,0,0,99,102,1,0,0,0,100,98,1,0,0,0,100,101,
        1,0,0,0,101,15,1,0,0,0,102,100,1,0,0,0,103,104,5,23,0,0,104,111,
        3,16,8,0,105,111,3,18,9,0,106,107,5,36,0,0,107,108,3,12,6,0,108,
        109,5,37,0,0,109,111,1,0,0,0,110,103,1,0,0,0,110,105,1,0,0,0,110,
        106,1,0,0,0,111,17,1,0,0,0,112,113,5,43,0,0,113,114,3,20,10,0,114,
        115,3,22,11,0,115,19,1,0,0,0,116,117,7,0,0,0,117,21,1,0,0,0,118,
        119,7,1,0,0,119,23,1,0,0,0,120,121,5,4,0,0,121,122,5,36,0,0,122,
        123,5,43,0,0,123,124,5,31,0,0,124,125,3,26,13,0,125,126,5,37,0,0,
        126,25,1,0,0,0,127,132,3,28,14,0,128,129,7,2,0,0,129,131,3,28,14,
        0,130,128,1,0,0,0,131,134,1,0,0,0,132,130,1,0,0,0,132,133,1,0,0,
        0,133,27,1,0,0,0,134,132,1,0,0,0,135,140,3,30,15,0,136,137,7,3,0,
        0,137,139,3,30,15,0,138,136,1,0,0,0,139,142,1,0,0,0,140,138,1,0,
        0,0,140,141,1,0,0,0,141,29,1,0,0,0,142,140,1,0,0,0,143,144,5,36,
        0,0,144,145,3,26,13,0,145,146,5,37,0,0,146,151,1,0,0,0,147,151,5,
        43,0,0,148,151,5,42,0,0,149,151,5,41,0,0,150,143,1,0,0,0,150,147,
        1,0,0,0,150,148,1,0,0,0,150,149,1,0,0,0,151,31,1,0,0,0,152,153,5,
        5,0,0,153,154,5,36,0,0,154,155,5,43,0,0,155,156,5,38,0,0,156,157,
        3,34,17,0,157,158,5,37,0,0,158,33,1,0,0,0,159,160,3,36,18,0,160,
        161,5,36,0,0,161,162,5,43,0,0,162,163,5,37,0,0,163,168,1,0,0,0,164,
        165,5,12,0,0,165,166,5,36,0,0,166,168,5,37,0,0,167,159,1,0,0,0,167,
        164,1,0,0,0,168,35,1,0,0,0,169,170,7,4,0,0,170,37,1,0,0,0,171,172,
        5,6,0,0,172,173,3,40,20,0,173,174,5,36,0,0,174,175,5,16,0,0,175,
        176,5,31,0,0,176,177,5,43,0,0,177,178,5,38,0,0,178,179,5,17,0,0,
        179,180,5,31,0,0,180,181,5,43,0,0,181,182,5,37,0,0,182,39,1,0,0,
        0,183,184,7,5,0,0,184,41,1,0,0,0,12,45,51,67,72,80,92,100,110,132,
        140,150,167
    ]

class VizFlowParser ( Parser ):

    grammarFileName = "VizFlowParser.g4"

    atn = ATNDeserializer().deserialize(serializedATN())

    decisionsToDFA = [ DFA(ds, i) for i, ds in enumerate(atn.decisionToState) ]

    sharedContextCache = PredictionContextCache()

    literalNames = [ "<INVALID>", "'DATASET'", "'LOAD'", "'FILTER'", "'TRANSFORM'", 
                     "'GROUP_BY'", "'PLOT'", "'DASHBOARD'", "'SUM'", "'AVG'", 
                     "'MIN'", "'MAX'", "'COUNT'", "'BAR'", "'LINE'", "'SCATTER'", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "<INVALID>", "<INVALID>", "<INVALID>", "<INVALID>", 
                     "'|>'", "'=='", "'!='", "'<='", "'>='", "'<'", "'>'", 
                     "'='", "'+'", "'-'", "'*'", "'/'", "'('", "')'", "','", 
                     "';'" ]

    symbolicNames = [ "<INVALID>", "DATASET", "LOAD", "FILTER", "TRANSFORM", 
                      "GROUP_BY", "PLOT", "DASHBOARD", "SUM", "AVG", "MIN", 
                      "MAX", "COUNT", "BAR", "LINE", "SCATTER", "X", "Y", 
                      "TRUE", "FALSE", "NULL", "AND", "OR", "NOT", "PIPE", 
                      "EQ", "NEQ", "LTE", "GTE", "LT", "GT", "ASSIGN", "PLUS", 
                      "MINUS", "STAR", "SLASH", "LPAREN", "RPAREN", "COMMA", 
                      "SEMI", "STRING_LIT", "FLOAT_LIT", "INT_LIT", "ID", 
                      "LINE_COMMENT", "BLOCK_COMMENT", "WS", "ERROR_CHAR" ]

    RULE_programa = 0
    RULE_sentencia = 1
    RULE_declaracionDataset = 2
    RULE_pipeline = 3
    RULE_operacion = 4
    RULE_filterOp = 5
    RULE_expresionLogica = 6
    RULE_expresionAnd = 7
    RULE_expresionNot = 8
    RULE_comparacion = 9
    RULE_operadorRelacional = 10
    RULE_valor = 11
    RULE_transformOp = 12
    RULE_expresionAritmetica = 13
    RULE_termino = 14
    RULE_factor = 15
    RULE_groupByOp = 16
    RULE_agregacion = 17
    RULE_funcionAgregacion = 18
    RULE_plotOp = 19
    RULE_tipoGrafico = 20

    ruleNames =  [ "programa", "sentencia", "declaracionDataset", "pipeline", 
                   "operacion", "filterOp", "expresionLogica", "expresionAnd", 
                   "expresionNot", "comparacion", "operadorRelacional", 
                   "valor", "transformOp", "expresionAritmetica", "termino", 
                   "factor", "groupByOp", "agregacion", "funcionAgregacion", 
                   "plotOp", "tipoGrafico" ]

    EOF = Token.EOF
    DATASET=1
    LOAD=2
    FILTER=3
    TRANSFORM=4
    GROUP_BY=5
    PLOT=6
    DASHBOARD=7
    SUM=8
    AVG=9
    MIN=10
    MAX=11
    COUNT=12
    BAR=13
    LINE=14
    SCATTER=15
    X=16
    Y=17
    TRUE=18
    FALSE=19
    NULL=20
    AND=21
    OR=22
    NOT=23
    PIPE=24
    EQ=25
    NEQ=26
    LTE=27
    GTE=28
    LT=29
    GT=30
    ASSIGN=31
    PLUS=32
    MINUS=33
    STAR=34
    SLASH=35
    LPAREN=36
    RPAREN=37
    COMMA=38
    SEMI=39
    STRING_LIT=40
    FLOAT_LIT=41
    INT_LIT=42
    ID=43
    LINE_COMMENT=44
    BLOCK_COMMENT=45
    WS=46
    ERROR_CHAR=47

    def __init__(self, input:TokenStream, output:TextIO = sys.stdout):
        super().__init__(input, output)
        self.checkVersion("4.13.1")
        self._interp = ParserATNSimulator(self, self.atn, self.decisionsToDFA, self.sharedContextCache)
        self._predicates = None




    class ProgramaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EOF(self):
            return self.getToken(VizFlowParser.EOF, 0)

        def sentencia(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.SentenciaContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.SentenciaContext,i)


        def getRuleIndex(self):
            return VizFlowParser.RULE_programa

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPrograma" ):
                listener.enterPrograma(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPrograma" ):
                listener.exitPrograma(self)




    def programa(self):

        localctx = VizFlowParser.ProgramaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 0, self.RULE_programa)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 43 
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while True:
                self.state = 42
                self.sentencia()
                self.state = 45 
                self._errHandler.sync(self)
                _la = self._input.LA(1)
                if not (_la==1 or _la==43):
                    break

            self.state = 47
            self.match(VizFlowParser.EOF)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class SentenciaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def declaracionDataset(self):
            return self.getTypedRuleContext(VizFlowParser.DeclaracionDatasetContext,0)


        def pipeline(self):
            return self.getTypedRuleContext(VizFlowParser.PipelineContext,0)


        def getRuleIndex(self):
            return VizFlowParser.RULE_sentencia

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterSentencia" ):
                listener.enterSentencia(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitSentencia" ):
                listener.exitSentencia(self)




    def sentencia(self):

        localctx = VizFlowParser.SentenciaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 2, self.RULE_sentencia)
        try:
            self.state = 51
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [1]:
                self.enterOuterAlt(localctx, 1)
                self.state = 49
                self.declaracionDataset()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 50
                self.pipeline()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class DeclaracionDatasetContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def DATASET(self):
            return self.getToken(VizFlowParser.DATASET, 0)

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(VizFlowParser.ASSIGN, 0)

        def LOAD(self):
            return self.getToken(VizFlowParser.LOAD, 0)

        def STRING_LIT(self):
            return self.getToken(VizFlowParser.STRING_LIT, 0)

        def SEMI(self):
            return self.getToken(VizFlowParser.SEMI, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_declaracionDataset

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterDeclaracionDataset" ):
                listener.enterDeclaracionDataset(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitDeclaracionDataset" ):
                listener.exitDeclaracionDataset(self)




    def declaracionDataset(self):

        localctx = VizFlowParser.DeclaracionDatasetContext(self, self._ctx, self.state)
        self.enterRule(localctx, 4, self.RULE_declaracionDataset)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 53
            self.match(VizFlowParser.DATASET)
            self.state = 54
            self.match(VizFlowParser.ID)
            self.state = 55
            self.match(VizFlowParser.ASSIGN)
            self.state = 56
            self.match(VizFlowParser.LOAD)
            self.state = 57
            self.match(VizFlowParser.STRING_LIT)
            self.state = 58
            self.match(VizFlowParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PipelineContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def PIPE(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.PIPE)
            else:
                return self.getToken(VizFlowParser.PIPE, i)

        def operacion(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.OperacionContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.OperacionContext,i)


        def SEMI(self):
            return self.getToken(VizFlowParser.SEMI, 0)

        def DASHBOARD(self):
            return self.getToken(VizFlowParser.DASHBOARD, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_pipeline

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPipeline" ):
                listener.enterPipeline(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPipeline" ):
                listener.exitPipeline(self)




    def pipeline(self):

        localctx = VizFlowParser.PipelineContext(self, self._ctx, self.state)
        self.enterRule(localctx, 6, self.RULE_pipeline)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 60
            self.match(VizFlowParser.ID)
            self.state = 61
            self.match(VizFlowParser.PIPE)
            self.state = 62
            self.operacion()
            self.state = 67
            self._errHandler.sync(self)
            _alt = self._interp.adaptivePredict(self._input,2,self._ctx)
            while _alt!=2 and _alt!=ATN.INVALID_ALT_NUMBER:
                if _alt==1:
                    self.state = 63
                    self.match(VizFlowParser.PIPE)
                    self.state = 64
                    self.operacion() 
                self.state = 69
                self._errHandler.sync(self)
                _alt = self._interp.adaptivePredict(self._input,2,self._ctx)

            self.state = 72
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            if _la==24:
                self.state = 70
                self.match(VizFlowParser.PIPE)
                self.state = 71
                self.match(VizFlowParser.DASHBOARD)


            self.state = 74
            self.match(VizFlowParser.SEMI)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def filterOp(self):
            return self.getTypedRuleContext(VizFlowParser.FilterOpContext,0)


        def transformOp(self):
            return self.getTypedRuleContext(VizFlowParser.TransformOpContext,0)


        def groupByOp(self):
            return self.getTypedRuleContext(VizFlowParser.GroupByOpContext,0)


        def plotOp(self):
            return self.getTypedRuleContext(VizFlowParser.PlotOpContext,0)


        def getRuleIndex(self):
            return VizFlowParser.RULE_operacion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperacion" ):
                listener.enterOperacion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperacion" ):
                listener.exitOperacion(self)




    def operacion(self):

        localctx = VizFlowParser.OperacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 8, self.RULE_operacion)
        try:
            self.state = 80
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [3]:
                self.enterOuterAlt(localctx, 1)
                self.state = 76
                self.filterOp()
                pass
            elif token in [4]:
                self.enterOuterAlt(localctx, 2)
                self.state = 77
                self.transformOp()
                pass
            elif token in [5]:
                self.enterOuterAlt(localctx, 3)
                self.state = 78
                self.groupByOp()
                pass
            elif token in [6]:
                self.enterOuterAlt(localctx, 4)
                self.state = 79
                self.plotOp()
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FilterOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def FILTER(self):
            return self.getToken(VizFlowParser.FILTER, 0)

        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def expresionLogica(self):
            return self.getTypedRuleContext(VizFlowParser.ExpresionLogicaContext,0)


        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_filterOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFilterOp" ):
                listener.enterFilterOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFilterOp" ):
                listener.exitFilterOp(self)




    def filterOp(self):

        localctx = VizFlowParser.FilterOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 10, self.RULE_filterOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 82
            self.match(VizFlowParser.FILTER)
            self.state = 83
            self.match(VizFlowParser.LPAREN)
            self.state = 84
            self.expresionLogica()
            self.state = 85
            self.match(VizFlowParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionLogicaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresionAnd(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.ExpresionAndContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.ExpresionAndContext,i)


        def OR(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.OR)
            else:
                return self.getToken(VizFlowParser.OR, i)

        def getRuleIndex(self):
            return VizFlowParser.RULE_expresionLogica

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpresionLogica" ):
                listener.enterExpresionLogica(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpresionLogica" ):
                listener.exitExpresionLogica(self)




    def expresionLogica(self):

        localctx = VizFlowParser.ExpresionLogicaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 12, self.RULE_expresionLogica)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 87
            self.expresionAnd()
            self.state = 92
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==22:
                self.state = 88
                self.match(VizFlowParser.OR)
                self.state = 89
                self.expresionAnd()
                self.state = 94
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionAndContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def expresionNot(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.ExpresionNotContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.ExpresionNotContext,i)


        def AND(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.AND)
            else:
                return self.getToken(VizFlowParser.AND, i)

        def getRuleIndex(self):
            return VizFlowParser.RULE_expresionAnd

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpresionAnd" ):
                listener.enterExpresionAnd(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpresionAnd" ):
                listener.exitExpresionAnd(self)




    def expresionAnd(self):

        localctx = VizFlowParser.ExpresionAndContext(self, self._ctx, self.state)
        self.enterRule(localctx, 14, self.RULE_expresionAnd)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 95
            self.expresionNot()
            self.state = 100
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==21:
                self.state = 96
                self.match(VizFlowParser.AND)
                self.state = 97
                self.expresionNot()
                self.state = 102
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionNotContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def NOT(self):
            return self.getToken(VizFlowParser.NOT, 0)

        def expresionNot(self):
            return self.getTypedRuleContext(VizFlowParser.ExpresionNotContext,0)


        def comparacion(self):
            return self.getTypedRuleContext(VizFlowParser.ComparacionContext,0)


        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def expresionLogica(self):
            return self.getTypedRuleContext(VizFlowParser.ExpresionLogicaContext,0)


        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_expresionNot

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpresionNot" ):
                listener.enterExpresionNot(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpresionNot" ):
                listener.exitExpresionNot(self)




    def expresionNot(self):

        localctx = VizFlowParser.ExpresionNotContext(self, self._ctx, self.state)
        self.enterRule(localctx, 16, self.RULE_expresionNot)
        try:
            self.state = 110
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [23]:
                self.enterOuterAlt(localctx, 1)
                self.state = 103
                self.match(VizFlowParser.NOT)
                self.state = 104
                self.expresionNot()
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 105
                self.comparacion()
                pass
            elif token in [36]:
                self.enterOuterAlt(localctx, 3)
                self.state = 106
                self.match(VizFlowParser.LPAREN)
                self.state = 107
                self.expresionLogica()
                self.state = 108
                self.match(VizFlowParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ComparacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def operadorRelacional(self):
            return self.getTypedRuleContext(VizFlowParser.OperadorRelacionalContext,0)


        def valor(self):
            return self.getTypedRuleContext(VizFlowParser.ValorContext,0)


        def getRuleIndex(self):
            return VizFlowParser.RULE_comparacion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterComparacion" ):
                listener.enterComparacion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitComparacion" ):
                listener.exitComparacion(self)




    def comparacion(self):

        localctx = VizFlowParser.ComparacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 18, self.RULE_comparacion)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 112
            self.match(VizFlowParser.ID)
            self.state = 113
            self.operadorRelacional()
            self.state = 114
            self.valor()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class OperadorRelacionalContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def EQ(self):
            return self.getToken(VizFlowParser.EQ, 0)

        def NEQ(self):
            return self.getToken(VizFlowParser.NEQ, 0)

        def LT(self):
            return self.getToken(VizFlowParser.LT, 0)

        def GT(self):
            return self.getToken(VizFlowParser.GT, 0)

        def LTE(self):
            return self.getToken(VizFlowParser.LTE, 0)

        def GTE(self):
            return self.getToken(VizFlowParser.GTE, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_operadorRelacional

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterOperadorRelacional" ):
                listener.enterOperadorRelacional(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitOperadorRelacional" ):
                listener.exitOperadorRelacional(self)




    def operadorRelacional(self):

        localctx = VizFlowParser.OperadorRelacionalContext(self, self._ctx, self.state)
        self.enterRule(localctx, 20, self.RULE_operadorRelacional)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 116
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 2113929216) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ValorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def INT_LIT(self):
            return self.getToken(VizFlowParser.INT_LIT, 0)

        def FLOAT_LIT(self):
            return self.getToken(VizFlowParser.FLOAT_LIT, 0)

        def STRING_LIT(self):
            return self.getToken(VizFlowParser.STRING_LIT, 0)

        def TRUE(self):
            return self.getToken(VizFlowParser.TRUE, 0)

        def FALSE(self):
            return self.getToken(VizFlowParser.FALSE, 0)

        def NULL(self):
            return self.getToken(VizFlowParser.NULL, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_valor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterValor" ):
                listener.enterValor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitValor" ):
                listener.exitValor(self)




    def valor(self):

        localctx = VizFlowParser.ValorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 22, self.RULE_valor)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 118
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 16492676251648) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TransformOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def TRANSFORM(self):
            return self.getToken(VizFlowParser.TRANSFORM, 0)

        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def ASSIGN(self):
            return self.getToken(VizFlowParser.ASSIGN, 0)

        def expresionAritmetica(self):
            return self.getTypedRuleContext(VizFlowParser.ExpresionAritmeticaContext,0)


        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_transformOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTransformOp" ):
                listener.enterTransformOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTransformOp" ):
                listener.exitTransformOp(self)




    def transformOp(self):

        localctx = VizFlowParser.TransformOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 24, self.RULE_transformOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 120
            self.match(VizFlowParser.TRANSFORM)
            self.state = 121
            self.match(VizFlowParser.LPAREN)
            self.state = 122
            self.match(VizFlowParser.ID)
            self.state = 123
            self.match(VizFlowParser.ASSIGN)
            self.state = 124
            self.expresionAritmetica()
            self.state = 125
            self.match(VizFlowParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class ExpresionAritmeticaContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def termino(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.TerminoContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.TerminoContext,i)


        def PLUS(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.PLUS)
            else:
                return self.getToken(VizFlowParser.PLUS, i)

        def MINUS(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.MINUS)
            else:
                return self.getToken(VizFlowParser.MINUS, i)

        def getRuleIndex(self):
            return VizFlowParser.RULE_expresionAritmetica

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterExpresionAritmetica" ):
                listener.enterExpresionAritmetica(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitExpresionAritmetica" ):
                listener.exitExpresionAritmetica(self)




    def expresionAritmetica(self):

        localctx = VizFlowParser.ExpresionAritmeticaContext(self, self._ctx, self.state)
        self.enterRule(localctx, 26, self.RULE_expresionAritmetica)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 127
            self.termino()
            self.state = 132
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==32 or _la==33:
                self.state = 128
                _la = self._input.LA(1)
                if not(_la==32 or _la==33):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 129
                self.termino()
                self.state = 134
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TerminoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def factor(self, i:int=None):
            if i is None:
                return self.getTypedRuleContexts(VizFlowParser.FactorContext)
            else:
                return self.getTypedRuleContext(VizFlowParser.FactorContext,i)


        def STAR(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.STAR)
            else:
                return self.getToken(VizFlowParser.STAR, i)

        def SLASH(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.SLASH)
            else:
                return self.getToken(VizFlowParser.SLASH, i)

        def getRuleIndex(self):
            return VizFlowParser.RULE_termino

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTermino" ):
                listener.enterTermino(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTermino" ):
                listener.exitTermino(self)




    def termino(self):

        localctx = VizFlowParser.TerminoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 28, self.RULE_termino)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 135
            self.factor()
            self.state = 140
            self._errHandler.sync(self)
            _la = self._input.LA(1)
            while _la==34 or _la==35:
                self.state = 136
                _la = self._input.LA(1)
                if not(_la==34 or _la==35):
                    self._errHandler.recoverInline(self)
                else:
                    self._errHandler.reportMatch(self)
                    self.consume()
                self.state = 137
                self.factor()
                self.state = 142
                self._errHandler.sync(self)
                _la = self._input.LA(1)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FactorContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def expresionAritmetica(self):
            return self.getTypedRuleContext(VizFlowParser.ExpresionAritmeticaContext,0)


        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def INT_LIT(self):
            return self.getToken(VizFlowParser.INT_LIT, 0)

        def FLOAT_LIT(self):
            return self.getToken(VizFlowParser.FLOAT_LIT, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_factor

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFactor" ):
                listener.enterFactor(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFactor" ):
                listener.exitFactor(self)




    def factor(self):

        localctx = VizFlowParser.FactorContext(self, self._ctx, self.state)
        self.enterRule(localctx, 30, self.RULE_factor)
        try:
            self.state = 150
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [36]:
                self.enterOuterAlt(localctx, 1)
                self.state = 143
                self.match(VizFlowParser.LPAREN)
                self.state = 144
                self.expresionAritmetica()
                self.state = 145
                self.match(VizFlowParser.RPAREN)
                pass
            elif token in [43]:
                self.enterOuterAlt(localctx, 2)
                self.state = 147
                self.match(VizFlowParser.ID)
                pass
            elif token in [42]:
                self.enterOuterAlt(localctx, 3)
                self.state = 148
                self.match(VizFlowParser.INT_LIT)
                pass
            elif token in [41]:
                self.enterOuterAlt(localctx, 4)
                self.state = 149
                self.match(VizFlowParser.FLOAT_LIT)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class GroupByOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def GROUP_BY(self):
            return self.getToken(VizFlowParser.GROUP_BY, 0)

        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def COMMA(self):
            return self.getToken(VizFlowParser.COMMA, 0)

        def agregacion(self):
            return self.getTypedRuleContext(VizFlowParser.AgregacionContext,0)


        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_groupByOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterGroupByOp" ):
                listener.enterGroupByOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitGroupByOp" ):
                listener.exitGroupByOp(self)




    def groupByOp(self):

        localctx = VizFlowParser.GroupByOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 32, self.RULE_groupByOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 152
            self.match(VizFlowParser.GROUP_BY)
            self.state = 153
            self.match(VizFlowParser.LPAREN)
            self.state = 154
            self.match(VizFlowParser.ID)
            self.state = 155
            self.match(VizFlowParser.COMMA)
            self.state = 156
            self.agregacion()
            self.state = 157
            self.match(VizFlowParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class AgregacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def funcionAgregacion(self):
            return self.getTypedRuleContext(VizFlowParser.FuncionAgregacionContext,0)


        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def ID(self):
            return self.getToken(VizFlowParser.ID, 0)

        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def COUNT(self):
            return self.getToken(VizFlowParser.COUNT, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_agregacion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterAgregacion" ):
                listener.enterAgregacion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitAgregacion" ):
                listener.exitAgregacion(self)




    def agregacion(self):

        localctx = VizFlowParser.AgregacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 34, self.RULE_agregacion)
        try:
            self.state = 167
            self._errHandler.sync(self)
            token = self._input.LA(1)
            if token in [8, 9, 10, 11]:
                self.enterOuterAlt(localctx, 1)
                self.state = 159
                self.funcionAgregacion()
                self.state = 160
                self.match(VizFlowParser.LPAREN)
                self.state = 161
                self.match(VizFlowParser.ID)
                self.state = 162
                self.match(VizFlowParser.RPAREN)
                pass
            elif token in [12]:
                self.enterOuterAlt(localctx, 2)
                self.state = 164
                self.match(VizFlowParser.COUNT)
                self.state = 165
                self.match(VizFlowParser.LPAREN)
                self.state = 166
                self.match(VizFlowParser.RPAREN)
                pass
            else:
                raise NoViableAltException(self)

        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class FuncionAgregacionContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def SUM(self):
            return self.getToken(VizFlowParser.SUM, 0)

        def AVG(self):
            return self.getToken(VizFlowParser.AVG, 0)

        def MIN(self):
            return self.getToken(VizFlowParser.MIN, 0)

        def MAX(self):
            return self.getToken(VizFlowParser.MAX, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_funcionAgregacion

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterFuncionAgregacion" ):
                listener.enterFuncionAgregacion(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitFuncionAgregacion" ):
                listener.exitFuncionAgregacion(self)




    def funcionAgregacion(self):

        localctx = VizFlowParser.FuncionAgregacionContext(self, self._ctx, self.state)
        self.enterRule(localctx, 36, self.RULE_funcionAgregacion)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 169
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 3840) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class PlotOpContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def PLOT(self):
            return self.getToken(VizFlowParser.PLOT, 0)

        def tipoGrafico(self):
            return self.getTypedRuleContext(VizFlowParser.TipoGraficoContext,0)


        def LPAREN(self):
            return self.getToken(VizFlowParser.LPAREN, 0)

        def X(self):
            return self.getToken(VizFlowParser.X, 0)

        def ASSIGN(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.ASSIGN)
            else:
                return self.getToken(VizFlowParser.ASSIGN, i)

        def ID(self, i:int=None):
            if i is None:
                return self.getTokens(VizFlowParser.ID)
            else:
                return self.getToken(VizFlowParser.ID, i)

        def COMMA(self):
            return self.getToken(VizFlowParser.COMMA, 0)

        def Y(self):
            return self.getToken(VizFlowParser.Y, 0)

        def RPAREN(self):
            return self.getToken(VizFlowParser.RPAREN, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_plotOp

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterPlotOp" ):
                listener.enterPlotOp(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitPlotOp" ):
                listener.exitPlotOp(self)




    def plotOp(self):

        localctx = VizFlowParser.PlotOpContext(self, self._ctx, self.state)
        self.enterRule(localctx, 38, self.RULE_plotOp)
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 171
            self.match(VizFlowParser.PLOT)
            self.state = 172
            self.tipoGrafico()
            self.state = 173
            self.match(VizFlowParser.LPAREN)
            self.state = 174
            self.match(VizFlowParser.X)
            self.state = 175
            self.match(VizFlowParser.ASSIGN)
            self.state = 176
            self.match(VizFlowParser.ID)
            self.state = 177
            self.match(VizFlowParser.COMMA)
            self.state = 178
            self.match(VizFlowParser.Y)
            self.state = 179
            self.match(VizFlowParser.ASSIGN)
            self.state = 180
            self.match(VizFlowParser.ID)
            self.state = 181
            self.match(VizFlowParser.RPAREN)
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx


    class TipoGraficoContext(ParserRuleContext):
        __slots__ = 'parser'

        def __init__(self, parser, parent:ParserRuleContext=None, invokingState:int=-1):
            super().__init__(parent, invokingState)
            self.parser = parser

        def BAR(self):
            return self.getToken(VizFlowParser.BAR, 0)

        def LINE(self):
            return self.getToken(VizFlowParser.LINE, 0)

        def SCATTER(self):
            return self.getToken(VizFlowParser.SCATTER, 0)

        def getRuleIndex(self):
            return VizFlowParser.RULE_tipoGrafico

        def enterRule(self, listener:ParseTreeListener):
            if hasattr( listener, "enterTipoGrafico" ):
                listener.enterTipoGrafico(self)

        def exitRule(self, listener:ParseTreeListener):
            if hasattr( listener, "exitTipoGrafico" ):
                listener.exitTipoGrafico(self)




    def tipoGrafico(self):

        localctx = VizFlowParser.TipoGraficoContext(self, self._ctx, self.state)
        self.enterRule(localctx, 40, self.RULE_tipoGrafico)
        self._la = 0 # Token type
        try:
            self.enterOuterAlt(localctx, 1)
            self.state = 183
            _la = self._input.LA(1)
            if not((((_la) & ~0x3f) == 0 and ((1 << _la) & 57344) != 0)):
                self._errHandler.recoverInline(self)
            else:
                self._errHandler.reportMatch(self)
                self.consume()
        except RecognitionException as re:
            localctx.exception = re
            self._errHandler.reportError(self, re)
            self._errHandler.recover(self, re)
        finally:
            self.exitRule()
        return localctx





