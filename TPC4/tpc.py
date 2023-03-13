import re

header_pattern = re.compile(r'(?P<name>[^,\n{}:]+)' \
           r'((({(?P<size>\d+)})|' \
           r'({(?P<min>\d+),(?P<max>\d+)}))' \
           r'(::(?P<function>[A-Za-z]+))?)?(,|$)')

atb_pattern = re.compile(r'(^|,)([^,\n]+)?')


def get_headers(fields):
    attributes_names = []
    for field in fields:
        if field['function']:
            attributes_names.append(field['name'] + '_' + field['function'])
        else:
            attributes_names.append(field['name'])
    return attributes_names

def _calculate_possible_none_idx():
    possible_none = []
    idx = 0
    for f in fields:
        if f['size']:
            idx += int(f['size'])
        elif f['max'] and f['min']:
            for i in range(int(f['min']), int(f['max'])):
                possible_none.append(idx + i)
            idx += int(f['max'])
        else:
            idx += 1
    return possible_none

def is_valid(possible_none, attributes):
    for i, val in enumerate(attributes):
        if val is None and i not in possible_none:
            return False
    return True

def calc_max_size():
    max_size = 0
    for f in fields:
        if f['size']:
            max_size += int(f['size'])
        elif f['max'] and f['min']:
            max_size += int(f['max'])
        else:
            max_size += 1
    return max_size

def _parse_list(attributes, max_size):
    parsed_list = []
    for i in range(0, max_size):
        if popped := attributes.pop(0):
            try:
                parsed_list.append(int(popped))
            except ValueError:
                try:
                    parsed_list.append(float(popped))
                except ValueError:
                    continue
    return parsed_list


def agregate_list(csv_list, agregation):
    if agregation and csv_list:
        if agregation == 'sum':
            return sum(csv_list)
        elif agregation == 'media':
            return sum(csv_list) / len(csv_list)
        elif agregation == 'max':
            return max(csv_list)
        elif agregation == 'min':
            return min(csv_list)
        elif agregation == 'len':
            return len(csv_list)


def parse_param(col, attributes):
    if col['size']:
        csv_list = _parse_list(attributes, int(col['size']))

    elif col['max'] and col['min']:
        csv_list = _parse_list(attributes, int(col['max']))

    else:
        return attributes.pop(0)

    if col['function']:
        return agregate_list(csv_list, col['function']) 
    else:
        return csv_list

def parse_header(line):
    fields = []
    for match in header_pattern.finditer(line):
        if list(filter(None, match.groupdict().values())):
            fields.append(match.groupdict())
    return fields

def parse_line(line, possible_none, fields):
    if not line or line.count(',') != calc_max_size() - 1:
        return False
    attributes = []

    for match in atb_pattern.finditer(line):
        attributes.append(match.group(2))
    
    if is_valid(possible_none, attributes):
        obj = []
        for col in fields:
            obj.append(parse_param(col, attributes))
        return obj

    return None

def write_attribute(F, tabs, col, attribute, end):
    for i in range(tabs):
        f.write('\t')
    attribute = f'"{col}": "{attribute}"'
    # checks if its is the end off the object
    if end:
        attribute += '\n'
    else:
        attribute += ',\n'
    f.write(attribute)

def write_obj(f,tabs,obj,atb_names):
    for i in range(tabs):
            f.write('\t')
    f.write("{\n")
    tabs += 1
    for i in range(len(atb_names)):
            write_attribute(f,tabs,atb_names[i], obj[i], i == len(atb_names) - 1)
    tabs -= 1
    for i in range(tabs):
            f.write('\t')
    f.write("}\n")

with open('data.txt') as f:
    fields = parse_header(f.readline())
    possible_none = _calculate_possible_none_idx()

    print(parse_line(f.readline(),possible_none, fields))
    print(fields)
    atb_names = get_headers(fields)
    with open("out.json","w") as out:
         tabs = 0
         out.write("[\n")
         tabs += 1
         for line in f :
             obj = parse_line(line,possible_none, fields)
             if obj:
                 write_obj(out,tabs,obj,atb_names)
         tabs -= 1
         out.write("]\n")
        
