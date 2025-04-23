from StaticError import *
from Symbol import *
from functools import *

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

def valid_assign_with_oldVariable(type, name,scopes):
    if not scopes:
        return False
    if name in scopes[-1]:
        if type == scopes[-1][name]["type"]:
            return True
        else:
            return False
    else:
        return valid_assign_with_oldVariable(type,name,scopes[:-1])

def assign_all_scopes(scopes, name, value,originscopes) -> int:
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
        
        if declared_type == "number":
            if (len(value) > 0 and all(c in "0123456789" for c in value)):
                current_scope[name]["value"] = value 
                return 3 #success
            if len(value) >2 and value[0] == "'" and value[-1] == "'":   
                inside = value[1:-1]
                if all(c.isalnum() or c == ' ' for c in inside):
                    return 1 #typeMis
        elif declared_type == "string":
            if len(value) >2 and value[0] == "'" and value[-1] == "'":   
                inside = value[1:-1]
                if all(c.isalnum() or c == ' ' for c in inside):
                    current_scope[name]["value"] = value 
                    return 3 #success
            if (len(value) > 0 and all(c in "0123456789" for c in value)):
                current_scope[name]["value"] = value 
                return 1 #typeMis
        return 2
    return assign_all_scopes(scopes[:-1], name, value,originscopes)

def check_redeclare(scopes, name):
    if name in scopes[-1]:
        return True
    return False

def is_valid_identifier(name: str) -> bool:
    return (name and name[0].islower() and all(c.isalnum() or c == '_' for c in name))

def is_valid_value(value: str) -> bool:
    if value[0] == "'" and value[-1] == "'":
        if not all(c.isalnum() or c == ' ' for c in value[1:-1]):
            return 0
    else:
        if not value.isdigit():
            return 0
    return 1
    
def count_spaces(s: str) -> int:
    return s.count(' ')

def check_insert_format(command: str) -> bool:
    parts = command.strip().split()
    return (len(parts) == 3 and parts[0] == "INSERT" and is_valid_identifier(parts[1]) and parts[2] in ["number", "string"])

def process_command(command, symbols, scopes):
    parts = command.strip().split()
    numspaces = count_spaces(command)

    if not parts or numspaces != len(parts) - 1:
        raise InvalidInstruction(command)

    if parts[0] == "INSERT":
        if not check_insert_format(command):
            raise InvalidInstruction(command)
        if check_redeclare(scopes, parts[1]):
            raise Redeclared(command)
        symbols.append(Symbol(parts[1], parts[2]))
        scopes[-1][parts[1]] = {"type": parts[2], "value": None}
        return "success", symbols, scopes

    elif parts[0] == "ASSIGN":
        if len(parts) < 3 or not is_valid_identifier(parts[1]):
            raise InvalidInstruction(command)
        name = parts[1]
        value = parts[2]
        result = assign_all_scopes(scopes, name, value,scopes)
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
        scopes.append({})
        return None, symbols, scopes

    elif parts[0] == "END":
        if len(parts) > 1: 
            raise InvalidInstruction(command)
        if len(scopes) > 1:
            scopes.pop()
            return None, symbols, scopes
        else:
            raise UnknownBlock()

    elif parts[0] == "LOOKUP":
        if len(parts) != 2 or not is_valid_identifier(parts[1]):
            raise InvalidInstruction(command)
        
        name = parts[1]
        scope_index = getIndex(scopes, name)  
        
        if scope_index != -1:
            return str(scope_index), symbols, scopes 
        else:
            raise Undeclared(command)
    elif parts[0] == "PRINT":
        if len(parts) > 1:
            raise InvalidInstruction(command)
        lists = getList([], scopes, symbols)
        result = " ".join(lists)
        return result, symbols, scopes
    elif parts[0] == "RPRINT":
        if len(parts) > 1:
            raise InvalidInstruction(command)
        lists = reversed(getList([], scopes, symbols))
        result = " ".join(lists)
        return result, symbols, scopes
    else: 
        raise InvalidInstruction(command)

# def process_commands(commands, result_list, symbols, scopes):
#     if not commands:
#         if len(scopes) > 1:
#             return process_commands(commands, result_list + [str(UnclosedBlock((len(scopes)-1)))], symbols, [{}])
#         return result_list
#     try:
#         result, new_symbols, new_scopes = process_command(commands[0], symbols, scopes)
#         if result is None:
#             return process_commands(commands[1:], result_list, new_symbols, new_scopes)
#         return process_commands(commands[1:], result_list + [result], new_symbols, new_scopes)
#     except StaticError as e:
#         return process_commands(commands[1:], result_list + [str(e)], symbols, scopes)
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
print(simulate(["INSERT x string", "INSERT y string", "BEGIN", "INSERT y number", "ASSIGN x y", "END"]))