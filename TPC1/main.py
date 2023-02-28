from math import floor

def ler_csv(file):
    pacientes = []
    min_colesterol = None;
    with open(file,"r") as f:
        cols = f.readline().replace("\n",'').split(",")
        for line in f.readlines():
            d = {}
            for k,v in zip(cols,line[:-1].split(",")):
                if k == "sexo":
                    d[k] = v
                else :
                    d[k] = int(v)
            if min_colesterol == None or d['colesterol'] < min_colesterol:
                min_colesterol = d['colesterol']
            pacientes.append(d)
    return pacientes,min_colesterol

def calcula_dist_sexo(pacientes,modelo):
    modelo['sexo'] = {"M": 0,"F": 0}
    m = 0
    f = 0
    for p in pacientes:
        if p['temDoença'] == 1:
            if p['sexo'] == "M": 
                modelo['sexo']['M']+=1
            elif p['sexo'] == "F": 
                modelo['sexo']['F']+=1

        if p['sexo'] == "M": 
                m+=1
        elif p['sexo'] == "F": 
                f+=1
        

    modelo['sexo']['M'] = modelo['sexo']['M'] / m * 100
    modelo['sexo']['F'] = modelo['sexo']['F'] / f * 100

def calcula_dist_idade(pacientes,modelo):
    modelo['idade'] = {}
    total = {}
    for p in pacientes:
        idade = p['idade']
        if idade >= 30 : 
            key = "{}-{}".format(floor(idade/5)*5, floor(idade/5)*5+4)

            if key in total:
                total[key] += 1
            else:
                total[key] = 1

            if p['temDoença'] == 1:
                if key in modelo['idade']:
                    modelo['idade'][key] += 1
                else:
                    modelo['idade'][key] = 1

    for k in modelo['idade']:
        modelo['idade'][k] = modelo['idade'][k]/total[k] *100

def calcula_dist_colesterol(pacientes,modelo,min):
    modelo['colesterol'] = {}
    for p in pacientes:
        colesterol = p['colesterol']
        key = "{}-{}".format(floor((colesterol-min_colesterol)/10)*10, floor((colesterol-min_colesterol)/10)*10+9)
        if key in modelo['colesterol']:
            modelo['colesterol'][key] += 1
        else:
            modelo['colesterol'][key] = 1
    for k in modelo['colesterol']:
        modelo['colesterol'][k] = modelo['colesterol'][k]/len(pacientes) *100
    return
            
def print_modelo(modelo):
    print("\t\t\tDistribuição por sexo\n")
    print("\t\t M \t F\n")
    print("\t\t{}%\t{}% \n\n".format(round(modelo['sexo']['M'],2), round(modelo['sexo']['F'],2)))

    print("\t\t\tDistribuição por idade\n")
    for k in modelo['idade']:
        print("\t{}".format(k),end='')
    print("\n")
    for k in modelo['idade']:
        print ("\t{}%".format(round(modelo['idade'][k],2)),end='')
    print("\n")

    print("\t\t\tDistribuição por colesterol\n")
    for k in modelo['colesterol']:
        print ("\t\t{}\t:\t{}%".format(k,round(modelo['colesterol'][k],2))) 
            
pacientes, min_colesterol = ler_csv("myheart.csv")       
modelo = {}
calcula_dist_sexo(pacientes, modelo)
calcula_dist_idade(pacientes, modelo)
calcula_dist_colesterol(pacientes, modelo, min_colesterol)
print_modelo(modelo)


