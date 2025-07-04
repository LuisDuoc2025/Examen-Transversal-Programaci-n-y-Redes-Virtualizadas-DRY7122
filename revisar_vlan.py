# revisar que tipo de vlan es
vlan = int(input("Ingrese el número de VLAN: "))

if 1 <= vlan <= 1005:
    print("La VLAN consultada es de rango estandar")
elif 1006 <= vlan <= 4094:
    print("La VLAN consultada es de rango extendido")
else:
    print("Número de VLAN inválido")

