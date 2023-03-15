import numpy as np
import os

def create_array(n,m):
    array1 = []
    for i in range(n):
        a = [0]*m
        array1.append(a)

    return array1

def open_file(name_file): #Funcion para abrir el archivo y extraer los datos mejorada respecto a la anterior
    ok=False
    
    try:
        open(name_file, "r")
        ok = True
    except FileNotFoundError:
        print("Archivo no encontrado")
        input("Presione enter para continuar...")
        
        
    if ok == True:
        print("Archivo cargado correctamente")
        with open(name_file, "r") as file_automata:
            cs = int(file_automata.readline()) 
            ce = int(file_automata.readline()) 
            rules = create_array(cs,ce)
            c, c_p1, c_p2 = 0, 0, 0
            automata = (linea for i, linea in enumerate(file_automata) if i>=0)

            for linea in automata:
                if len(linea)>1:
                    if c_p1 == 0:
                        if "Sig{" in linea: 
                            i1 = linea.index('{')
                            i2 = linea.index('}')
                            sig = linea[i1+1:i2].split(",")
                            c_p1 += 1

                    if c_p2 == 0:
                        if "F{" in linea:
                            i1 = linea.index('{')
                            i2 = linea.index('}')
                            f = linea[i1+1:i2].split(',')
                            c_p2 += 1

                    if '>' in linea: 
                        i1 = linea.index('>')
                        if ',' in linea:
                            i2 = linea.index(',')
                        elif '}' in linea:
                            i2 = linea.index('}')
                        rules[c] = linea[i1+1:i2].split('|')
                        c+=1

            i = 0
            while i < len(rules):
                j = 0
                while j < len(rules[i]):  
                    c_space = str(rules[i][j]).count(" ")
                    rules[i][j] = str(rules[i][j]).replace(" ","",c_space)
                    j += 1
                i += 1
        try:
            return sig,f,rules
        except UnboundLocalError:
            print("Archivo no valido, sintaxis inapropiada")
            input("Presione enter para continuar...")
            return 0,0,0
    
    else:
        return 0,0,0

def evaluate_string(str_evaluate,sigma,f,rules):
    str_valid = True
    list_pos_car, list_states1,list_states2,list_states = [], [], [], ["0"]

    for i in str_evaluate:
        if i in sigma:
            x = 0
            if 0 == len(list_states): 
                print("\nResultados -> ['NULL']")
                print("\nCadena no valida")
                input("Presione enter para continuar...")
                str_valid = False
                break
            else:
                while x < len(list_states): 
                    list_pos_car.append(sigma.index(i))
                    list_states1.append(rules[int(list_states[x])][list_pos_car[0]])

                    if list_states1[x] != "NULL": 
                        var_str = list_states1[x]

                        c = 0
                        while c < len(var_str):
                            list_states2.append(var_str[c])
                            c += 1
                    x += 1

                list_pos_car.clear()
                list_states1.clear()
                list_states.clear()

                c = 0
                while c < len(list_states2):
                    list_states.append(list_states2[c])
                    c += 1
                list_states = list(np.sort(list(set(list_states))))
                list_states2.clear()

        else:
            print(f"\nCadena no valida, el caracter '{i}' no pertenece a Sigma {sigma}") 
            str_valid = False
            input("Presione enter para continuar...")
            break
        
    if str_valid == True:
        if 0 == len(list_states):
            print(f"\nResultados -> ['NULL']")
            print("\nCadena no valida")
            input("Presione enter para continuar...")
        else: 
            print(f"\nResultados -> {list_states}")

            c = 0
            while c < len(list_states): 
                if list_states[c] in f:
                    print("\nCadena valida")
                    input("Presione enter para continuar...")
                    break  

                if c+1 == len(list_states): 
                    print("\nCadena no valida")
                    input("Presione enter para continuar...")
                    break

                c += 1

def main():
    clearConsole = lambda: os.system('cls' if os.name in ('nt', 'dos') else 'clear')
    aut_loaded = False

    c = 0
    while c == 0:
        if aut_loaded == False:
            print("\n-- MENU --")
            print("1- CARGAR AUTOMATA")
            print("2- SALIR")

            try:
                op = int(input("\nINGRESE EL NUMERO DE LA OPCION: "))
            except ValueError:
                print("Ingrese un numero valido")
                op = 0
                input("Presione enter para continuar...")
                clearConsole()
                
            if op == 1:
                name_file = input("Ingresa el nombre del automata: ")
                clearConsole()
                sigma, f, rules = open_file(name_file)
                if sigma == 0:
                    aut_loaded = False
                    clearConsole()
                else:
                    aut_loaded = True

            elif op == 2:
                c = 1
                break

        elif aut_loaded == True:
            print(f"\nSigma -> {sigma}")
            print(f"Estados Finales -> {f}")
            print(f"Reglas -> {rules}")

            print("\n-- Elija, por favor --")
            print("1- Elegir otro automata")
            print("2- Comprobar cadena")
            print("3- Salir")

            op = int(input("\nIngrese su selección: "))

            if op == 1:
                name_file = input("Ingresa el nombre del otro automata: ")
                clearConsole()
                sigma, f, rules = open_file(name_file)

            elif op == 2:
                str_evaluate = input("Ingrese la cadena a evaluar: ")
                evaluate_string(str_evaluate,sigma,f,rules)
                clearConsole()
            
            elif op == 3:
                c = 1
                break

if __name__ == "__main__":
    main()
