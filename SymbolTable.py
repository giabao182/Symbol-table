from StaticError import *
from Symbol import *
from functools import *

# def getList(lists, scopes, symbols):
#     if not scopes:
#         return lists
#     scope = scopes[-1]
#     keys = list(scope.keys())
#     for key in reversed(keys):
#         if any(sym.name == key for sym in symbols):
#             lists.insert(0, f"{key}//{len(scopes) - 1}")
#             symbols = [s for s in symbols if s.name != key]
#     return getList(lists, scopes[:-1], symbols)
def process_keys(i, keys, scopes, symbols, lists):
    if i < 0:
        return lists, symbols
    key = keys[i]
    if any(sym.name == key for sym in symbols):
        lists.insert(0, f"{key}//{len(scopes) - 1}")
        symbols = [s for s in symbols if s.name != key]
    return process_keys(i - 1, keys, scopes, symbols, lists)

def getList(lists, scopes, symbols):
    if not scopes:
        return lists
    scope = scopes[-1]
    keys = list(scope.keys())
    lists, symbols = process_keys(len(keys) - 1, keys, scopes, symbols, lists)
    return getList(lists, scopes[:-1], symbols)

def getIndex(scopes, name) -> int:
    if not scopes:
        return -1
    if name in scopes[-1]:
        return len(scopes) - 1
    else:
        return getIndex(scopes[:-1],name)
def assign_all_scopes(scopes, name, value) -> int:
    if not scopes:
        return 0 
    
    current_scope = scopes[-1]
    if name in current_scope:
        declared_type = current_scope[name]["type"] 
        
        if declared_type == "number":
            if not value.isdigit():
                return 1 
        elif declared_type == "string":
            if value.isdigit():
                return 1 
        
        current_scope[name]["value"] = value 
        return 3 
    return assign_all_scopes(scopes[:-1], name, value) or 0
def check_redeclare(symbols, scopes, name):
    return name in scopes[-1] if scopes else False

def is_valid_identifier(name: str) -> bool:
    return (name and name[0].islower() and all(c.isalnum() or c == '_' for c in name))

def check_insert_format(command: str) -> bool:
    parts = command.strip().split()
    return (len(parts) == 3 and parts[0] == "INSERT" and is_valid_identifier(parts[1]) and parts[2] in ["number", "string"])

def process_command(command, symbols, scopes):
    parts = command.strip().split()
    
    if not parts:
        return InvalidInstruction(command), symbols, scopes

    if parts[0] == "INSERT":
        if not check_insert_format(command):
            return InvalidInstruction(command), symbols, scopes
        if check_redeclare(symbols, scopes, parts[1]):
            return Redeclared(command), symbols, scopes
        symbols.append(Symbol(parts[1], parts[2]))
        scopes[-1][parts[1]] = {"type": parts[2], "value": None}
        return "success", symbols, scopes

    elif parts[0] == "ASSIGN":
        if len(parts) < 3 or not is_valid_identifier(parts[1]):
            return InvalidInstruction(command), symbols, scopes
        
        name = parts[1]
        value = parts[2]
        result = assign_all_scopes(scopes, name, value)
        
        if result == 0:
            return Undeclared(command), symbols, scopes
        elif result == 1:
            return TypeMismatch(command), symbols, scopes
        else:
            return "success", symbols, scopes

    elif parts[0] == "BEGIN":
        scopes.append({})
        return None, symbols, scopes

    elif parts[0] == "END":
        if len(scopes) > 1:
            scopes.pop()
            return None, symbols, scopes
        else:
            return UnknownBlock(), symbols, scopes

    elif parts[0] == "LOOKUP":
        if len(parts) != 2:
            return InvalidInstruction(command), symbols, scopes
        
        name = parts[1]
        scope_index = getIndex(scopes, name)  
        
        if scope_index != -1:
            return str(scope_index), symbols, scopes 
        else:
            return Undeclared(command), symbols, scopes
    elif parts[0] == "PRINT":
        lists = getList([], scopes, symbols)
        result = " ".join(lists)
        return result, symbols, scopes
    elif parts[0] == "RPRINT":
        lists = reversed(getList([], scopes, symbols))
        result = " ".join(lists)
        return result, symbols, scopes

def process_commands(commands, result_list, symbols, scopes):
    if not commands:
        return result_list
    result, new_symbols, new_scopes = process_command(commands[0], symbols, scopes)
    formatted_result = str(result) if isinstance(result, StaticError) else result
    if formatted_result == None:
        return process_commands(commands[1:], 
                          result_list, 
                          new_symbols, 
                          new_scopes)
    return process_commands(commands[1:], 
                          result_list + [formatted_result], 
                          new_symbols, 
                          new_scopes)

def simulate(list_of_commands):
    return process_commands(list_of_commands, [], [], [{}])