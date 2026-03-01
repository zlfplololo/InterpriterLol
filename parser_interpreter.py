#parser_interpriter.py
import tokenizer as tk
import re
variables = {}
TokenType, Abstractype = tk.GTT()
def Mathparcify(exp):
    res = exp.copy()
    for i in range(len(res)):
        if res[i]["TYPE"].name == TokenType.NUMBER.name:
            res[i] = float(res[i]['value'])
        elif res[i]["TYPE"].name == TokenType.STRING.name:
            res[i] = res[i]["value"]
        elif res[i]["TYPE"].name == Abstractype.LIST.name:
            res[i] = res[i]["items"]
        else:
            match res[i]["TYPE"].name:
                case TokenType.PLUS.name:
                    res[i] = "+"
                case TokenType.MINUS.name:
                    res[i] = "-"
                case TokenType.MULTIPLY.name:
                    res[i] = '*'
                case TokenType.DIVIDE.name:
                    res[i] = '/'
                case TokenType.EXPONANT.name:
                    res[i] = "^"
                case TokenType.EQ.name:
                    res[i] = "=="
                case TokenType.BEQ.name:
                    res[i] = ">="
                case TokenType.LEQ.name:
                    res[i] = "<="
                case TokenType.NEQ.name:
                    res[i] = "!="
                case TokenType.MODULO.name:
                    res[i] = "%"
                case TokenType.BIN_SHIFT_LEFT.name:
                    res[i] = '<<'
                case TokenType.BIN_SHIFT_RIGHT.name:
                    res[i] = ">>"
                case TokenType.BIGGER.name:
                    res[i] = '>'
                case TokenType.SMALLER.name:
                    res[i] = '<'
                case TokenType.OPENING_BRACKET.name:
                    res[i] = '('
                case TokenType.CLOSING_BRACKET.name:
                    res[i] = ')'
    return res
def BT(a):
    result = a.copy()

    # --- Bracket grouping (unchanged) ---
    i = len(result) -1
    scc = 0
    sc = False
    scp = [0,0]
    scpL = []
    while i >= 0:
        if not sc:
            if result[i] == ")":
                sc = True
                scp[1] = i
        else:
            if result[i] == ")":
                scc +=1
            if result[i] == "(":
                if scc >0:
                    scc-=1
                else:
                    sc = False
                    scp[0] = i
                    scpL.append(scp.copy())
        i-=1

    for i in scpL:
        result[i[0]:i[1]+1] = BT(result[i[0]+1:i[1]])

    # --- Operator grouping left to right ---
    def group_ops(result, ops):
        i = 0
        while i < len(result) - 2:
            if type(result[i]) in (float, list, str):
                if result[i+1] in ops:
                    if type(result[i+2]) in (float, list, str):
                        result[i:i+3] = [[result[i], result[i+1], result[i+2]]]
                        # stay at same index to handle nested/grouped ops
                        continue
            i += 1
        return result

    for ops in [["^"], ["*", "/"], ["+", "-"], ["%"], ["<<", ">>"], ["<", ">", "==", "<=", ">=", "!="]]:
        result = group_ops(result, ops)

    return result

def execME(a):
    res = a.copy()
    error = [False, "",  []]
    def Process(a):
        error = [False, "",  []]
        if type(a[0]) == float:
            if type(a[2]) == float:
                match a[1]:
                    case '^':
                        return a[0] ** a[2], error
                    case '*':
                        return a[0] * a[2], error
                    case '/':
                        return a[0] / a[2], error
                    case "+" :
                        return a[0] + a[2], error
                    case "-":
                        return a[0] - a[2], error
                    case "%":
                        return a[0] % a[2], error
                    case "<<":
                        def binshiftleft(num, val):
                            naf = 0
                            while num * (10**naf) % 1 > 0:
                                naf +=1
                            num *= 10**naf
                            num = (int(num) << val) / (10**naf)
                            return num
                        try:
                            return binshiftleft(a[0], int(a[2])), error
                        except ValueError:
                            return 0, [True, 'CBSFNOT', []]
                    case ">>":
                        def binshiftright(num, val):
                            naf = 0
                            while num * (10**naf) % 1 > 0:
                                naf +=1
                            num *= 10**naf
                            num = (int(num) >> val) / (10**naf)
                            return num
                        try:
                            return binshiftright(a[0], int(a[2])), error
                        except ValueError:
                            return 0, [True, 'CBSFNOT', []]
                    case "==":
                        return a[0] == a[2], error
                    case "<":
                        return a[0] < a[2], error
                    case ">":
                        return a[0] > a[2], error
                    case "<=":
                        return a[0] <= a[2], error
                    case ">=":
                        return a[0] >= a[2], error
                    case "!=":
                        return a[0] != a[2], error
                    case _:
                        return 0, [True, "IOO", [a[1]]]
            else:
                return 0, [True, "ISDTC", [type(a[2])]]
        if type(a[0]) == str:
            if type(a[2]) == str:
                match a[1]:
                    case "==":
                        return a[0] == a[2], error
                    case "!=":
                        return a[0] != a[2], error
                    case "+":
                        return a[0] + a[2], error
                    case _:
                        return 0, [True, "IOO", [a[1]]]
            elif type(a[2]) == float:
                match a[1]:
                    case "*":
                        return a[0] * int(a[2]), error
                    case _:
                        return 0, [True, "IOO", [a[1]]]
            else:
                return 0, [True, "ISDTC", [type(a[2])]]
        if type(a[0]) == list:
            if type(a[2]) == list:
                match a[1]:
                    case "==":
                        return a[0] == a[2], error
                    case "!=":
                        return a[0] != a[2], error
                    case "+":
                        return a[0] + a[2], error
                    case _:
                        return 0, [True, "IOO", [a[1]]]
            elif type(a[2]) == float:
                match a[1]:
                    case "*":
                        return a[0] * int(a[2]), error
                    case _:
                        return 0, [True, "IOO", [a[1]]]
            else:
                return 0, [True, "ISDTC", [type(a[2])]]
    if not error[0]:
        if type(res[0]) is list and len(res[0]) == 3:
            isaproglist = False
            for i in res[0]:
                if type(i) != float and len(i)>0 and type(i[0]) is dict:
                    isaproglist = True
            if not isaproglist:
                res[0], error = execME(res[0])
    if not error[0]:
        if type(res[2]) is list and len(res[2]) == 3 :
            isaproglist = False
            for i in res[2]:
                if type(i) != float and len(i)>0 and type(i[0]) is dict:
                    isaproglist = True
            if not isaproglist:
                res[2], error = execME(res[2])
    if not error[0]:
        toret, error = Process(res)
        return toret, error

class Interpriter():
    def Inxecute(self, arg):
        global TokenType, variables
        trash = ''
        error = [False, "", []]
        argC = arg.copy()
        for i in range(len(argC)):
            match argC[i]["TYPE"].name:
                case TokenType.SET.name:
                    return 0, [True, "NPCOA", [TokenType.SET]] #non-parsable collection of arguments
                case TokenType.SET_REFERENCE.name:
                    return 0, [True, "NPCOA", [TokenType.DIVIDER]] #non-parsable collection of arguments
                case Abstractype.SETVAR.name:
                    return 0, [True, "NPCOA", [Abstractype.SETVAR]] #non-parsable collection of arguments
                case Abstractype.SETREFVAR.name:
                    return 0, [True, "NPCOA", [Abstractype.SETREFVAR]] #non-parsable collection of arguments
                case Abstractype.REFERENCE.name:
                    if len(argC) > 1 or argC[i]['value']['TYPE'].name != TokenType.UNDEFINED_EXPRESSION.name:
                        val, error = self.Inxecute([argC[i]['value']])
                        argC[i] = val[0]
                case Abstractype.CALL.name:
                    trash, argC[i] = self.interpret([argC[i]])
                    if trash == -2:
                        return 0, [True, "_", []]
                case Abstractype.GETINDEX.name:
                    argC[i]['name'], error = self.Inxecute(argC[i]['name'])
                    for j in range(len(argC[i]['value'])):
                        argC[i]['value'][j], error = self.Inxecute(argC[i]['value'][j])
                    if not error[0]:
                        selectedval = argC[i]['name'][0]
                        for j in range(len(argC[i]['value'])):
                            if selectedval['TYPE'].name == Abstractype.LIST.name:
                                if argC[i]['value'][j][0]['TYPE'].name == TokenType.NUMBER.name:
                                    if re.fullmatch(r'\d+(\.0)?', argC[i]['value'][j][0]['value']):
                                        try:
                                            selectedval = selectedval["items"][int(float(argC[i]['value'][j][0]['value']))][0]
                                        except IndexError:
                                            try:
                                                trash = selectedval["items"][int(float(argC[i]['value'][j][0]['value']))]
                                            except IndexError:
                                                return 0, [True, "LIOOR", [argC[i]['value'][j][0]['value']]]
                                            else:
                                                selectedval = tk.execute_tokenizer("0")[0]
                                    else:
                                        return 0, [True, "IFNE", []]
                                else: return 0, [True, "NCDT", [argC[i]['value'][0]['TYPE']]]
                            else:
                                return 0, [True, "NCDT", [selectedval["TYPE"]]]
                        argC[i] = selectedval
                    else: return 0, error
                case TokenType.UNDEFINED_EXPRESSION.name:
                    var_name = argC[i]["value"]
                    if var_name in variables:
                        argC[i] = variables[var_name]
                    else:
                        return 0, [True, "NVF", [var_name]]
                case Abstractype.GROUP.name:
                    argC[i]['value'], error = self.Inxecute(argC[i]['value'])
                case Abstractype.LIST.name:
                    for j in range(len(argC[i]["items"])):
                        argC[i]["items"][j], error = self.Inxecute(argC[i]["items"][j])
                case TokenType.CLOSING_BRACKET.name:
                    return 0, [True, "UCB", []] #unmatched closing bracket
                case TokenType.CLOSING_SQUARE_BRACKET.name:
                    return 0, [True, "UCSB", []] #unmatched closing square bracket
                case TokenType.OPENING_BRACKET.name:
                    return 0, [True, "UOB", []] #unmatched opening bracket
                case TokenType.OPENING_SQUARE_BRACKET.name:
                    return 0, [True, "UOSB", []] #unmatched opening bracket
            
        def AC(argC):
            error = [True, '', []]
            argD = argC.copy()
            def GTBVB(arg):
                argC = arg.copy()
                i = len(argC) -1
                while i >= 0:
                    if argC[i]['TYPE'].name == Abstractype.GROUP.name:
                        val = argC[i]['value']
                        val.insert(0, {'TYPE': TokenType.OPENING_BRACKET})
                        val.append({'TYPE': TokenType.CLOSING_BRACKET})
                        argC[i:i+1] = val
                    i-=1
                return argC
            havegroup = True
            while havegroup:
                havegroup = False
                for i in argD:
                    if i["TYPE"].name == Abstractype.GROUP.name:
                        havegroup = True
                        break
                if havegroup:
                    argD = GTBVB(argD)
            def removebrackets(arg):
                argC = arg.copy()
                i = len(argC) -1
                while i >= 0:
                    if argC[i]["TYPE"].name == TokenType.OPENING_BRACKET.name or argC[i]["TYPE"].name == TokenType.CLOSING_BRACKET.name:
                        argC.pop(i)
                    i-=1
                return argC
            nobrackets = removebrackets(argD)
            for i in range(len(nobrackets)):
                if not i%2:
                    match nobrackets[i]["TYPE"].name:
                        case TokenType.NUMBER.name:
                            pass
                        case TokenType.STRING.name:
                            pass
                        case Abstractype.LIST.name:
                            pass
                        case _:
                            return 0, [True, "WOOF", [nobrackets[i]["TYPE"].name]]
                else:
                    match nobrackets[i]["TYPE"].name:
                        case TokenType.EXPONANT.name:
                            pass
                        case TokenType.MULTIPLY.name:
                            pass
                        case TokenType.DIVIDE.name:
                            pass
                        case TokenType.PLUS.name:
                            pass
                        case TokenType.MINUS.name:
                            pass
                        case TokenType.MODULO.name:
                            pass
                        case TokenType.BIN_SHIFT_LEFT.name:
                            pass
                        case TokenType.BIN_SHIFT_RIGHT.name:
                            pass
                        case TokenType.EQ.name:
                            pass
                        case TokenType.BIGGER.name:
                            pass
                        case TokenType.SMALLER.name:
                            pass
                        case TokenType.LEQ.name:
                            pass
                        case TokenType.BEQ.name:
                            pass
                        case TokenType.NEQ.name:
                            pass
                        case _:
                            return 0, [True, "WOOF", [nobrackets[i]["TYPE"].name]]

            if nobrackets[-1:][0]["TYPE"].name != TokenType.NUMBER.name and nobrackets[-1:][0]["TYPE"].name != TokenType.STRING.name and nobrackets[-1:][0]["TYPE"].name != Abstractype.LIST.name:
                return 0, [True, "ICL", []]
            argD, error = execME(BT(Mathparcify(argD))[0])
            if not error[0]:
                if type(argD) == float:
                    argD = tk.execute_tokenizer(f"{argD}")[0]
                elif type(argD) == bool:
                    if argD:
                        argD = tk.execute_tokenizer("1")[0]
                    else:
                        argD = tk.execute_tokenizer("0")[0]
                elif type(argD) == str:
                    argD = tk.execute_tokenizer(f"{'"' if not ('"' in argD) else "'"}{argD}{'"' if not ('"' in argD) else "'"}")[0]
                elif type(argD) == list:
                    argD = [{"TYPE": Abstractype.LIST, 'items': argD}]
            return argD, error
        while not error[0] and len(argC) > 1:
            argC, error = AC(argC)
        return argC, error

    def interpret(self, truetokens):
        global TokenType, variables
        error = [False, "", []]
        tokens = truetokens.copy()
        for token in tokens:
            match token["TYPE"].name:
                case Abstractype.CALL.name:
                    match token["name"]:
                        case "write":
                            if len(token["args"]) == 1:
                                token["args"][0], error = self.Inxecute(token["args"][0])
                                if not error[0]:
                                    for arg in token["args"]:
                                        match arg[0]["TYPE"].name:
                                            case TokenType.STRING.name:
                                                print(arg[0]["value"])
                                            case TokenType.NUMBER.name:
                                                print(arg[0]["value"])
                                            case Abstractype.LIST.name:
                                                def listtoprint(lista):
                                                    composedtoprint = '['
                                                    for i in range(len(lista)):
                                                        val = lista[i][0]
                                                        match val["TYPE"].name:
                                                            case TokenType.NUMBER.name:
                                                                composedtoprint += val['value']
                                                            case TokenType.STRING.name:
                                                                composedtoprint += val['value']
                                                            case Abstractype.LIST.name:
                                                                composedtoprint = listtoprint(val['items'])
                                                        if i != len(lista)-1:
                                                            composedtoprint += ", "
                                                    composedtoprint += ']'
                                                    return composedtoprint
                                                print(listtoprint(arg[0]['items']))
                                            case Abstractype.REFERENCE.name:
                                                self.Inxecute([{"TYPE": Abstractype.CALL, 'name': 'write', 'args':[[arg[0]['value']]]}])
                            else:
                                error = [True, "INOA", []] #incorrect number of arguments

                        case "goto":
                            if len(token["args"]) == 1:
                                token["args"][0], error = self.Inxecute(token["args"][0])
                                if not error[0]:
                                    for arg in token["args"]:
                                        match arg[0]["TYPE"].name:
                                            case TokenType.NUMBER.name:
                                                if re.fullmatch(r'\d+(\.0+)?', arg[0]['value']):
                                                    return int(float(arg[0]['value'])), 0
                                                else:
                                                    error = [True, "GFNE", [arg[0]['value']]] #goto fractional number exception
                                            case _:
                                                error = [True, "NCDT", [arg[0]["TYPE"]]]
                                                break
                            else:
                                error = [True, "INOA", []] #incorrect number of arguments

                        case "get":
                            if len(token["args"]) == 1:
                                token["args"][0], error = self.Inxecute(token["args"][0])
                                if not error[0]:
                                    for arg in token["args"]:
                                        match arg[0]["TYPE"].name:
                                            case TokenType.STRING.name:
                                                res = input(arg[0]['value'])
                                                return -3, tk.execute_tokenizer(f"{'"' if "'" in res else "'"}{res}{'"' if "'" in res else "'"}")[0][0]
                                            case _:
                                                error = [True, "NCDT", [arg[0]["TYPE"]]]
                                                break
                            else:
                                error = [True, "INOA", []] #incorrect number of arguments
                        case 'getnum':
                            if len(token["args"]) == 1:
                                token["args"][0], error = self.Inxecute(token["args"][0])
                                if not error[0]:
                                    for arg in token["args"]:
                                        match arg[0]["TYPE"].name:
                                            case TokenType.STRING.name:
                                                res = input(arg[0]['value'])
                                                if re.fullmatch(r'-?\d+(\.\d+)?', res):
                                                    return -3, tk.execute_tokenizer(f"{res}")[0][0]
                                                else:
                                                    error = [True, "NAN", [res]]
                                            case _:
                                                error = [True, "NCDT", [arg[0]["TYPE"]]]
                                                break
                            else:
                                error = [True, "INOA", []] #incorrect number of arguments
                        case _:
                            error = [True, "UF", [f"{token["name"]}()"]]

                case Abstractype.SETVAR.name:
                    if token['value'][0]["TYPE"].name != Abstractype.REFERENCE.name or not (token['value'][0]["value"]['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or token['value'][0]["value"]['TYPE'].name == Abstractype.GETINDEX.name):
                        token["value"], error = self.Inxecute(token["value"])
                    if not error[0]:
                        if token["name"]["TYPE"].name == TokenType.UNDEFINED_EXPRESSION.name:
                            if token["name"]["value"] in variables:
                                var = variables[token['name']['value']]
                                if var["TYPE"].name == Abstractype.REFERENCE.name and (var['value']['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or var['value']['TYPE'].name == Abstractype.GETINDEX.name):
                                    self.interpret([{"TYPE": Abstractype.SETVAR, 'name': var['value'], 'value': token['value']}])
                                elif not (var == Abstractype.REFERENCE.name or (var == TokenType.UNDEFINED_EXPRESSION.name or var == Abstractype.GETINDEX.name)):
                                    variables[token['name']['value']] = token['value'][0]    
                            else:
                                variables[token['name']['value']] = token['value'][0]
                        elif token["name"]["TYPE"].name == Abstractype.GETINDEX.name:
                            if token["name"]['name'][0]['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name:
                                if token["name"]["name"][0]["value"] in variables:
                                    tokencompiled, error = self.Inxecute(token['name']['name'])
                                    if not error[0]:
                                        selectedval = tokencompiled[0]
                                        for j in range(len(token['name']['value'])):
                                            if selectedval['TYPE'].name == Abstractype.LIST.name:
                                                if token['name']['value'][j][0]['TYPE'].name == TokenType.NUMBER.name:
                                                    if re.fullmatch(r'\d+(\.0)?', token['name']['value'][j][0]['value']):
                                                        try:
                                                            selectedval = selectedval["items"][int(float(token['name']['value'][j][0]['value']))][0]
                                                        except IndexError:
                                                            try:
                                                                selectedval = selectedval["items"][int(float(token['name']['value'][j][0]['value']))]
                                                            except IndexError:
                                                                error = [True, "LIOOR", [token['name']['value'][j][0]['value']]]
                                                                break
                                                            else:
                                                                selectedval = tk.execute_tokenizer("0")[0]
                                                    else:
                                                        error = [True, "IFNE", []]
                                                        break
                                                else:
                                                    error = [True, "NCDT", [token['value'][0]['value'][0]['TYPE']]]
                                                    break
                                            else:
                                                error = [True, "NCDT", [selectedval["TYPE"]]]
                                                break
                                        if not error[0]:
                                            if selectedval["TYPE"].name == Abstractype.REFERENCE.name and (selectedval['value']['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or selectedval['value']['TYPE'].name == Abstractype.GETINDEX.name):
                                                self.interpret([{"TYPE": Abstractype.SETVAR, 'name': selectedval['value'], 'value': token['value']}])
                                            else:
                                                newvalue = tokencompiled[0]
                                                toproc = newvalue
                                                for j in range(len(token['name']['value'])-1):
                                                    if selectedval['TYPE'].name == Abstractype.LIST.name:
                                                        if token['name']['value'][j][0]['TYPE'].name == TokenType.NUMBER.name:
                                                            if re.fullmatch(r'\d+(\.0)?', token['name']['value'][j][0]['value']):
                                                                try:
                                                                    toproc = toproc["items"][int(float(token['name']['value'][j][0]['value']))][0]
                                                                except IndexError:
                                                                    try:
                                                                        toproc = toproc["items"][int(float(token['name']['value'][j][0]['value']))]
                                                                    except IndexError:
                                                                        error = [True, "LIOOR", [token['name']['value'][j][0]['value']]]
                                                                        break
                                                                    else:
                                                                        toproc = tk.execute_tokenizer("0")[0]
                                                            else:
                                                                error = [True, "IFNE", []]
                                                                break
                                                        else:
                                                            error = [True, "NCDT", [token['value'][0]['value'][0]['TYPE']]]
                                                            break
                                                    else:
                                                        error = [True, "NCDT", [selectedval["TYPE"]]]
                                                        break
                                                toproc["items"][int(float(token['name']['value'][-1][0]['value']))] = token['value']
                        else:
                            error = [True, "CS", [token["name"]["TYPE"]]]
                case Abstractype.SETREFVAR.name:
                    if token['value'][0]["TYPE"].name != Abstractype.REFERENCE.name or not (token['value'][0]["value"]['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or token['value'][0]["value"]['TYPE'].name == Abstractype.GETINDEX.name):
                        token["value"], error = self.Inxecute(token["value"])
                    if not error[0]:
                        if token["name"]["TYPE"].name == TokenType.UNDEFINED_EXPRESSION.name:
                            if token["name"]["value"] in variables:
                                var = variables[token['name']['value']]
                                if var["TYPE"].name == Abstractype.REFERENCE.name and (var['value']['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or var['value']['TYPE'].name == Abstractype.GETINDEX.name):
                                    variables[token['name']['value']] = token['value'][0]   
                                elif not (var == Abstractype.REFERENCE.name and (var == TokenType.UNDEFINED_EXPRESSION.name or var == Abstractype.GETINDEX.name)):
                                    error = [True, "CRNRVV", []] # cannot reset non-reference variable value
                            else:
                                variables[token['name']['value']] = token['value'][0]
                        elif token["name"]["TYPE"].name == Abstractype.GETINDEX.name:
                            if token["name"]['name'][0]['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name:
                                if token["name"]["name"][0]["value"] in variables:
                                    tokencompiled, error = self.Inxecute(token['name']['name'])
                                    if not error[0]:
                                        selectedval = tokencompiled[0]
                                        for j in range(len(token['name']['value'])):
                                            if selectedval['TYPE'].name == Abstractype.LIST.name:
                                                if token['name']['value'][j][0]['TYPE'].name == TokenType.NUMBER.name:
                                                    if re.fullmatch(r'\d+(\.0)?', token['name']['value'][j][0]['value']):
                                                        try:
                                                            selectedval = selectedval["items"][int(float(token['name']['value'][j][0]['value']))][0]
                                                        except IndexError:
                                                            try:
                                                                selectedval = selectedval["items"][int(float(token['name']['value'][j][0]['value']))]
                                                            except IndexError:
                                                                error = [True, "LIOOR", [token['name']['value'][j][0]['value']]]
                                                                break
                                                            else:
                                                                selectedval = tk.execute_tokenizer("0")[0]
                                                    else:
                                                        error = [True, "IFNE", []]
                                                        break
                                                else:
                                                    error = [True, "NCDT", [token['value'][0]['value'][0]['TYPE']]]
                                                    break
                                            else:
                                                error = [True, "NCDT", [selectedval["TYPE"]]]
                                                break
                                        if not error[0]:
                                            if selectedval["TYPE"].name == Abstractype.REFERENCE.name and (selectedval['value']['TYPE'].name == TokenType.UNDEFINED_EXPRESSION.name or selectedval['value']['TYPE'].name == Abstractype.GETINDEX.name):
                                                newvalue = tokencompiled[0]
                                                toproc = newvalue
                                                for j in range(len(token['name']['value'])-1):
                                                    if selectedval['TYPE'].name == Abstractype.LIST.name:
                                                        if token['name']['value'][j][0]['TYPE'].name == TokenType.NUMBER.name:
                                                            if re.fullmatch(r'\d+(\.0)?', token['name']['value'][j][0]['value']):
                                                                try:
                                                                    toproc = toproc["items"][int(float(token['name']['value'][j][0]['value']))][0]
                                                                except IndexError:
                                                                    try:
                                                                        toproc = toproc["items"][int(float(token['name']['value'][j][0]['value']))]
                                                                    except IndexError:
                                                                        error = [True, "LIOOR", [token['name']['value'][j][0]['value']]]
                                                                        break
                                                                    else:
                                                                        toproc = tk.execute_tokenizer("0")[0]
                                                            else:
                                                                error = [True, "IFNE", []]
                                                                break
                                                        else:
                                                            error = [True, "NCDT", [token['value'][0]['value'][0]['TYPE']]]
                                                            break
                                                    else:
                                                        error = [True, "NCDT", [selectedval["TYPE"]]]
                                                        break
                                                toproc["items"][int(float(token['name']['value'][-1][0]['value']))] = token['value']
                                            else:
                                                error = [True, "CRNRVV", []] # cannot reset non-reference variable value
                        else:
                            error = [True, "CS", [token["name"]["TYPE"]]]
        if error[0]:
            match error[1]:
                case "NVF":
                    print(f"No Variable found under the name: '{error[2][0]}'")
                case "ISDTIC":
                    print(f"Incorrect second datatype in collection, the Incorrect datatype is: {error[2][0]}")
                case "NICOA":
                    print(f"Non-parsable collection of arguments, the one whitch had triggered the error is: {error[2][0]}")
                case "WOOF":
                    print(f"Wrong order of collection, this occured because the {error[2][0]} has occured in the wrong place")
                case "NCDT":
                    print(f"Non-Compatable Data Type, whitch is: {error[2][0]}")
                case "IOO":
                    print(f"Incompatable operator operator: {error[2][0]}")
                case "IO":
                    print(f"Incompatable operation: {error[2][0]}")
                case "CS":
                    print(f"Cannot set {error[2][0]}")
                case "CRNRVV":
                    print("Cannot reset non-reference variable value")
                case "ICL":
                    print("Incompatable collection length")
                case "INOA":
                    print("Incorrect number of arguments")
                case "GFNE":
                    print("Goto fractional number exception")
                case "IFNE":
                    print("Index fractional number exception")
                case "NPCOA":
                    print("non-parsable collection of arguments")
                case "LIOOR":
                    print("List index out of range")
                case "UF":
                    print(f"Undefined function: {error[2][0]}")
                case "UCB":
                    print("Unmatched closing bracket")
                case "UOB":
                    print("Unmatched opening bracket")
                case "NAN":
                    print(f"Not a Number: {error[2][0]}")
                case "CBSFNOT":
                    print(f"cannot binary shift a fractional number of times")
                case "":
                    print("This program has suffered major brain damage")

            return -2, 0
        return -1, 0
if __name__ == "__main__":
    itpt =  Interpriter()
    tokens0 = tk.execute_tokenizer("a = getnum('hello!: ')")[0]
    tokens1 = tk.execute_tokenizer("b = ~a")[0]
    tokens2 = tk.execute_tokenizer("write(1 << 1)")[0]
    #print(tokens2)
    itpt.interpret(tokens0)
    itpt.interpret(tokens1)
    itpt.interpret(tokens2)
    print(variables)