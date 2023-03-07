import re


def get_seculo(data):
    return (data[0] - 1 )// (100 + 1)

def get_first_last(name):
    if pat_first_last.match(name):
        return tuple(pat_first_last.match(name).groups())
    else:
        return None
    
pat = re.compile(r'^(\d+)::(\d{4})-(\d{2})-(\d{2})::([^:]+)::([^:]+)::([^:]+)::::$')
pat_first_last  = re.compile(r'^(\w+)\b.*\b(\w+)?$')
regs = []
p_freq = {}
nome_freq = {}



with open("TPC3/processos.txt", "r") as f:
    
    for line in f:
       if pat.match(line.strip()):
            values = pat.match(line.strip()).groups()
            reg = {
                'n_processos' : int(values[0]),
                'data' : tuple(map(int,values[1:4])),
                'nome' : values[4:7],
            }
            p_freq[reg['data'][0]] = p_freq.get(reg['data'][0],0) + reg['n_processos']
            first, last = get_first_last(reg['nome'][0])

            if get_seculo(reg['data']) in nome_freq:
                nome_freq[get_seculo(reg['data'])][first] = nome_freq[get_seculo(reg['data'])].get(first,0) + 1
                nome_freq[get_seculo(reg['data'])][last] = nome_freq[get_seculo(reg['data'])].get(last,0) + 1
            else:
                nome_freq[get_seculo(reg['data'])] = {first: 1, last: 1}
            

            regs.append(reg)

print(nome_freq)