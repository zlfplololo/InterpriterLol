#Tokenizer.py
import re
import enum

def both(lista):
    for i in range(len(lista)):
        yield i, lista[i] 

def splitlistby(lista, by):
    newlist = []
    listpoints = [-1,]
    for i, val in both(lista):
        if val == by:
            listpoints.append(i)
    for i, val in both(listpoints):
        if i != len(listpoints)-1:
            newlist.append(lista[val+1: listpoints[i+1]])
        else:
            newlist.append(lista[val+1: len(lista)])
    return newlist


def GTT():
    class TokenType(enum.Enum):
        STOP_SET = r"\$=;"
        EQ = r'=='
        NEQ = r'!='
        BEQ = r'>='
        LEQ = r'=<'
        BIN_SHIFT_RIGHT = r">>"
        BIN_SHIFT_LEFT = r'<<'
        SET_REFERENCE = r'~='
        OPENING_BRACKET = r'\('
        CLOSING_BRACKET = r'\)'
        OPENING_SQUARE_BRACKET = r'\['
        CLOSING_SQUARE_BRACKET = r'\]'
        PLUS = r'\+'
        MINUS = r'-'
        MULTIPLY = r'\*'
        DIVIDE = r'/'
        EXPONANT = r'\^'
        BIGGER = r">"
        SMALLER = r'<'
        MODULO = r'%'
        SET = r'='
        NUMBER = r'\d+(\.\d+)?'
        STRING = r"('[^']*')|(\"[^\"]*\")"
        UNDEFINED_EXPRESSION = r'\w+'
        REFERENCE_SYMBOL = r"~"
        COMMA = r','
        DIVIDER = r';'
        NEWLINE = r'\n'
        COMMENT = r'#.*\n'
    class AbstractType(enum.Enum):
        GROUP = 0
        INDEX = 1
        COLLECTION = 2
        LIST = 3
        CALL = 4
        GETINDEX = 5
        REFERENCE = 6
        SETVAR = 7
        SETREFVAR = 8
    return TokenType, AbstractType

def execute_tokenizer(string):
    class TOKENIZER:
        def __init__(self, tokentype):
            self.tokentype, self.abstractype = tokentype
        

        def compile(self, string):
            string = re.sub(r"[     ]+(?=(?:(?:[^\"']*[\"']){2})*[^\"']*$)", "", string)
            tokens = []
            pos = 0
            while pos < len(string):
                match_found = False
                for token in self.tokentype:
                    pattern = re.compile(token.value)
                    m = pattern.match(string, pos)
                    if m:
                        match_found = True
                        value = m.group(0)
                        match token:
                            case self.tokentype.NUMBER:
                                tokens.append({"TYPE": token, 'value': value})
                            case self.tokentype.STRING:
                                val = value[1:-1]
                                tokens.append({"TYPE": token, 'value': val})
                            case self.tokentype.UNDEFINED_EXPRESSION:
                                tokens.append({"TYPE": token, 'value': value})
                            case self.tokentype.DIVIDER:
                                pass
                            case self.tokentype.COMMENT:
                                pass
                            case _:
                                tokens.append({"TYPE": token})
                        pos += len(value)
                        break
                if not match_found:
                    # If no token matched, skip one character (to avoid infinite loop)
                    pos += 1
            return tokens
                
        def group_brackets(self, tokens):
            result = tokens.copy()

            i = len(result) -1
            scc = 0
            sc = False
            scp = [0,0]
            scpL = []
            while i >= 0:
                if not sc:
                    if result[i]["TYPE"] == self.tokentype.CLOSING_BRACKET:
                        sc = True
                        scp[1] = i
                else:
                    if result[i]["TYPE"] == self.tokentype.CLOSING_BRACKET:
                        scc +=1
                    if result[i]["TYPE"] == self.tokentype.OPENING_BRACKET:
                        if scc >0:
                            scc-=1
                        else:
                            sc = False
                            scp[0] = i
                            scpL.append(scp.copy())
                i-=1

            for i in scpL:
                result[i[0]:i[1]+1] = self.RSN([{"TYPE": self.abstractype.GROUP, "value": self.AllProc(result[i[0]+1:i[1]])}])
            
            i = len(result) -1
            qscc = 0
            qsc = False
            qscp = [0,0]
            qscpL = []
            while i >= 0:
                if not qsc:
                    if result[i]["TYPE"] == self.tokentype.CLOSING_SQUARE_BRACKET:
                        qsc = True
                        qscp[1] = i
                else:
                    if result[i]["TYPE"] == self.tokentype.CLOSING_SQUARE_BRACKET:
                        qscc +=1
                    if result[i]["TYPE"] == self.tokentype.OPENING_SQUARE_BRACKET:
                        if qscc >0:
                            qscc-=1
                        else:
                            qsc = False
                            qscp[0] = i
                            qscpL.append(qscp.copy())
                i-=1

            for i in qscpL:
                result[i[0]:i[1]+1] = self.RSN([{"TYPE": self.abstractype.INDEX, "value": self.AllProc(result[i[0]+1:i[1]])}])

            return result

        def BTC(self, tokens):
            result = tokens.copy()
            for i, val in both(result):
                isacollectione = False
                if val["TYPE"] == self.abstractype.GROUP:
                    for j in val['value']:
                        if j['TYPE'] == self.tokentype.COMMA:
                            isacollectione = True
                    if isacollectione:
                        result[i] = {"TYPE": self.abstractype.COLLECTION, 'value': [self.AllProc(i, last=True) for i in splitlistby(val['value'], {"TYPE": self.tokentype.COMMA})]}
                if val["TYPE"] == self.abstractype.INDEX:
                    for j in val['value']:
                        if j['TYPE'] == self.tokentype.COMMA:
                            isacollectione = True
                    if isacollectione:
                        result[i] = {"TYPE": self.abstractype.LIST, 'items': [self.AllProc(i, last=True) for i in splitlistby(val['value'], {"TYPE": self.tokentype.COMMA})]}
            return result
        
        def Proc(self, tokens):
            result = tokens.copy()
            i = len(result) -1
            isalredyminused = False
            while i > 0:
                isalredyminused = False
                if result[i]["TYPE"] == self.abstractype.COLLECTION or result[i]["TYPE"] == self.abstractype.GROUP:
                    match result[i-1]["TYPE"]:
                        case self.tokentype.UNDEFINED_EXPRESSION:
                            result[i-1:i+1] = [{"TYPE": self.abstractype.CALL, 'name': result[i-1]['value'], 'args': [self.RIT(j) for j in result[i]['value']] if result[i]["TYPE"] == self.abstractype.COLLECTION else [self.RIT(result[i]['value'])]}]
                    i-=1
                    isalredyminused = True
                if result[i]["TYPE"] == self.abstractype.INDEX:
                    if result[i-1]['TYPE'] == self.tokentype.UNDEFINED_EXPRESSION or result[i-1]['TYPE'] == self.abstractype.LIST or result[i-1] == self.abstractype.INDEX:
                        result[i-1:i+1] = [{"TYPE": self.abstractype.GETINDEX, 'name': [result[i-1]], 'value': [result[i]['value']]}]
                        i-=1
                        isalredyminused = True
                        while result[i]['name'][0]["TYPE"] == self.abstractype.INDEX and result[i-1]['TYPE'] == self.tokentype.UNDEFINED_EXPRESSION or result[i-1]['TYPE'] == self.abstractype.LIST or result[i-1] == self.abstractype.INDEX and i > 0:
                            result[i-1:i+1] = [{"TYPE": self.abstractype.GETINDEX, 'name': [result[i-1]], 'value': result[i]['value']+[result[i]['name'][0]['value']]}]
                            i-=1
                        result[i]['name'] = self.RIT(result[i]['name'])
                        for j in range(len(result[i]["value"])):
                            result[i]['value'][j] = self.RIT(result[i]["value"][j])
                if result[i-1]["TYPE"] == self.tokentype.REFERENCE_SYMBOL:
                    result[i-1:i+1] = [{"TYPE": self.abstractype.REFERENCE, 'value': self.RIT([result[i]])[0]}]
                    i-=1
                    isalredyminused = True
                if result[i]["TYPE"] == self.tokentype.REFERENCE_SYMBOL:
                    result[i:i+2] = [{"TYPE": self.abstractype.REFERENCE, 'value': self.RIT([result[i+1]])[0]}]
                    i-=1
                    isalredyminused = True
                if i > 1:
                    if result[i]['TYPE'] == self.tokentype.NUMBER and result[i-1]['TYPE'] == self.tokentype.MINUS and result[i-2]['TYPE'] != self.tokentype.NUMBER:
                        result[i-1:i+1] = [{'TYPE': self.tokentype.NUMBER, 'value': f'-{result[i]['value']}'}]
                elif i > 0:
                    if result[i]['TYPE'] == self.tokentype.NUMBER and result[i-1]['TYPE'] == self.tokentype.MINUS:
                        result[i-1:i+1] = [{'TYPE': self.tokentype.NUMBER, 'value': f'-{result[i]['value']}'}]
                if not isalredyminused:
                    i-=1
            i = len(result) -1
            isalredyminused = False
            while i > 0:
                isalredyminused = False
                if result[i]['TYPE'] == self.tokentype.SET:
                    value = [i+1,-1]
                    for j in range(i, len(result)):
                        if result[j]["TYPE"] == self.tokentype.STOP_SET or result[j]["TYPE"] == self.tokentype.NEWLINE:
                            value[1] = j
                            if result[j]["TYPE"] == self.tokentype.NEWLINE:
                                remainlastone = True
                            else:
                                remainlastone = False
                            break
                    result[i-1:len(result) if value[1] < 0 else value[1]+1 if not remainlastone else value[1]] = [{"TYPE": self.abstractype.SETVAR, "name": result[i-1], "value": self.RIT(result[value[0]:len(result) if value[1] < 0 else value[1]])}]
                    i-=1
                    isalredyminused = True
                if result[i]['TYPE'] == self.tokentype.SET_REFERENCE:
                    value = [i+1,-1]
                    for j in range(i, len(result)):
                        if result[j]["TYPE"] == self.tokentype.STOP_SET or result[j]["TYPE"] == self.tokentype.NEWLINE:
                            value[1] = j
                            if result[j]["TYPE"] == self.tokentype.NEWLINE:
                                remainlastone = True
                            else:
                                remainlastone = False
                            break
                    result[i-1:len(result) if value[1] < 0 else value[1]+1 if not remainlastone else value[1]] = [{"TYPE": self.abstractype.SETREFVAR, "name": result[i-1], "value": self.RIT(result[value[0]:len(result) if value[1] < 0 else value[1]])}]
                    i-=1
                    isalredyminused = True
                if not isalredyminused:
                    i-=1
            return result
        def RIT(self, tokens, leaveN = False):
            result = tokens.copy()
            i = len(result)-1
            while i >= 0:
                match result[i]['TYPE']:
                    case self.tokentype.NEWLINE:
                        if not leaveN:
                            result.pop(i)
                    case self.tokentype.REFERENCE_SYMBOL:
                        result.pop(i)
                    case self.tokentype.STOP_SET:
                        result.pop(i)
                    case self.tokentype.COMMA:
                        result.pop(i)
                i-=1
            for i, val in both(result):
                match val['TYPE']:
                    case self.abstractype.COLLECTION:
                        result[i] = {'TYPE':self.abstractype.LIST, 'items': val['value']}
                    case self.abstractype.INDEX:
                        result[i] = {'TYPE':self.abstractype.LIST, 'items': [val['value']] if len(val['value']) > 0 else []}
            return result
        def RSN(self, tokens):
            result = tokens.copy()
            i = len(result)-1
            while i >= 0:
                match result[i]['TYPE']:
                    case self.tokentype.NEWLINE:
                        result.pop(i)
                i-=1
            return result
        def AllProc(self, tokens, last = False, splitbySN = False):
            if last:
                if not splitbySN:
                    return self.RIT(self.Proc(self.BTC(self.group_brackets(tokens))))
                else:
                    return splitlistby(self.RIT(self.Proc(self.BTC(self.group_brackets(tokens))), leaveN=True), self.compile('\n')[0])
            else:
                return self.Proc(self.BTC(self.group_brackets(tokens)))
    tokenizer = TOKENIZER(GTT())
    return tokenizer.AllProc(tokenizer.compile(string), last=True, splitbySN=True)

if __name__ == "__main__":
    print(execute_tokenizer('''
                            # assling
                            write(a)
                            a = 1
                            write(i)'''))
