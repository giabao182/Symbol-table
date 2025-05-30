from StaticError import *
from Symbol import *
from functools import *

def process_keys(i, keys, scopes, symbols, lists):
    if i < 0:
        return lists, symbols
    key = keys[i]
    if any(sym.name == key for sym in symbols):
        lists = [f"{key}//{len(scopes) - 1}"] + lists
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

def check_assign(scopes, name, value,originscopes) -> int:
    if not scopes:
        return 0 #Undeclare
    current_scope = scopes[-1]
    if name in current_scope:
        declared_type = current_scope[name]["type"] 
        
        value_index = getIndex(originscopes, value)
        if value_index != -1:
            value_type = originscopes[value_index][value]["type"]
            if declared_type == value_type:
                current_scope[name]["value"] = value
                return 3  # success
            else:
                return 1  # type mismatch
        if is_valid_identifier(value):
            return 0

        if declared_type == "number":
            if (len(value) > 0 and all(c in "0123456789" for c in value)):
                current_scope[name]["value"] = value 
                return 3 #success
            if len(value) >2 and value[0] == "'" and value[-1] == "'":   
                if all(c.isalnum() or c == ' ' for c in value[1:-1]):
                    return 1 #typeMis
        elif declared_type == "string":
            if len(value) >2 and value[0] == "'" and value[-1] == "'":   
                if all(c.isalnum() or c == ' ' for c in value[1:-1]):
                    current_scope[name]["value"] = value 
                    return 3 #success
            if (len(value) > 0 and all(c in "0123456789" for c in value)):
                current_scope[name]["value"] = value 
                return 1 #typeMis
        return 2
    return check_assign(scopes[:-1], name, value,originscopes)

def is_valid_identifier(name: str) -> bool:
    return (name and name[0].islower() and all(c.isalnum() or c == '_' for c in name))

def process_command(command, symbols, scopes):
    parts = command.strip().split()
    numspaces = command.count(' ')

    if not parts or numspaces != len(parts) - 1:
        raise InvalidInstruction(command)

    if parts[0] == "INSERT":
        if not (len(parts) == 3 and parts[0] == "INSERT" and is_valid_identifier(parts[1]) and parts[2] in ["number", "string"]):
            raise InvalidInstruction(command)
        if parts[1] in scopes[-1]:
            raise Redeclared(command)
        symbols = symbols + [Symbol(parts[1], parts[2])]
        return "success", symbols, scopes[:-1] + [{**scopes[-1], parts[1]: {"type": parts[2], "value": None}}]

    elif parts[0] == "ASSIGN":
        if len(parts) < 3 or not is_valid_identifier(parts[1]):
            raise InvalidInstruction(command)
        result = check_assign(scopes, parts[1], parts[2],scopes)
        if result == 0:
            raise Undeclared(command)
        elif result == 1:
            raise TypeMismatch(command)
        elif result == 2:
            raise InvalidInstruction(command)
        else:
            return "success", symbols, scopes

    elif parts[0] == "BEGIN":
        if len(parts) > 1: 
            raise InvalidInstruction(command)
        return None, symbols, scopes + [{}]

    elif parts[0] == "END":
        if len(parts) > 1: 
            raise InvalidInstruction(command)
        if len(scopes) > 1:
            return None, symbols, scopes[:-1]
        else:
            raise UnknownBlock()

    elif parts[0] == "LOOKUP":
        if len(parts) != 2 or not is_valid_identifier(parts[1]):
            raise InvalidInstruction(command)
        
        scope_index = getIndex(scopes, parts[1])  
        
        if scope_index != -1:
            return str(scope_index), symbols, scopes 
        else:
            raise Undeclared(command)
    elif parts[0] == "PRINT":
        if len(parts) > 1:
            raise InvalidInstruction(command)
        return " ".join(getList([], scopes, symbols)), symbols, scopes
    elif parts[0] == "RPRINT":
        if len(parts) > 1:
            raise InvalidInstruction(command)
        return " ".join(list(reversed(getList([], scopes, symbols)))), symbols, scopes
    else: 
        raise InvalidInstruction(command)

def process_commands(commands, result_list, symbols, scopes):
    if not commands:
        if len(scopes) > 1:
            return [str(UnclosedBlock(len(scopes) - 1))]  
        return result_list
    try:
        result, new_symbols, new_scopes = process_command(commands[0], symbols, scopes)
        if result is None:
            return process_commands(commands[1:], result_list, new_symbols, new_scopes)
        return process_commands(commands[1:], result_list + [result], new_symbols, new_scopes)
    except StaticError as e:
        return [str(e)]  


def simulate(list_of_commands):
    return process_commands(list_of_commands, [], [], [{}])