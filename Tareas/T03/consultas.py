from principal import (parientes_grado_1, parientes_grado0, parientes_grado1,
                       parientes_grado2, parientes_gradon, personas)
from math import sqrt
from functools import reduce
from collections import *
import json


def pariente_de(grado, persona):
    if grado == "-1":
        respuesta = tuple(parientes[1].nombre for parientes in
                          parientes_grado_1 if parientes[0].nombre == persona)
    elif grado == "0":
        respuesta = tuple(parientes[1].nombre for parientes in
                          parientes_grado0 if parientes[0].nombre == persona)
    elif grado == "1":
        respuesta = tuple(parientes[1].nombre for parientes in
                          parientes_grado1 if parientes[0].nombre == persona)
    elif grado == "2":
        respuesta = tuple(parientes[1].nombre for parientes in
                          parientes_grado2 if parientes[0].nombre == persona)
    elif grado == "n":
        respuesta = tuple(parientes[1].nombre for parientes in
                          parientes_gradon if parientes[0].nombre == persona)
    return respuesta


def ascendencia(persona):
    ascendencias = []
    #persona = list(perse for perse in personas if perse.nombre == persona)
    #pers = persona[0]
    personaa = filter(lambda x: x.nombre == persona, personas)
    pers = next(personaa)
    if pers.pelo == "negro" and "pecho" in pers.vello and pers.nariz == "recta":
        ascendencias.append("mediterranea")
    if pers.pelo == "negro" and pers.piel == "negro" and pers.pie >= 44:
        ascendencias.append("africana")
    if pers.guata == "guaton" and "espalda" in pers.vello:
        ascendencias.append("estadounidense")
    if ("AAT" in pers.caracteristicas["GTC"] and
            "AAT" in pers.caracteristicas["GGA"] and "AAT"
            in pers.caracteristicas["TCT"]):
        ascendencias.append("albina")
    return ascendencias


def índice_de_tamaño(persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    genes_tamaño_altura = persona.caracteristicas["AAG"].count("AGT")
    genes_tamaño_guata = persona.caracteristicas["TGG"].count("AGT")
    opuestos_tamaño_altura = persona.caracteristicas["AAG"].count("ACT")
    opuestos_tamaño_guata = persona.caracteristicas["TGG"].count("ACT")
    porcentaje_altura = genes_tamaño_altura / (genes_tamaño_altura +
                                               opuestos_tamaño_altura)
    porcentaje_guata = genes_tamaño_guata / (genes_tamaño_guata +
                                             opuestos_tamaño_guata)
    indice = sqrt(porcentaje_altura * porcentaje_guata)
    return indice


def contador_total(persona, otra_persona):
    contadores = (contador_por_caract(persona, otra_persona, caracteristica)
                  for caracteristica in persona.caracteristicas)
    contador_total = reduce(lambda x, y: x + y, contadores)
    return contador_total


def contador_por_caract(persona, otra_persona, caracteristica):
    genes_persona = Counter(persona.caracteristicas[caracteristica])
    genes_otra_persona = Counter(otra_persona.caracteristicas[caracteristica])
    contador_por_gen = (min(cantidad, genes_otra_persona[tag]) for tag, cantidad in genes_persona.items())
    contador = reduce(lambda x, y: x + y, contador_por_gen)
    return contador


def gemelo_genético(persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    #lista = [(otra_persona, contador_total(persona, otra_persona))
    #         for otra_persona in personas if otra_persona != persona]
    # lista es una lista de tuplas con (persona, contador genes parecidos)
    #lista.sort(key=lambda x: x[1], reverse = True)
    lista = ((otra_persona, contador_total(persona, otra_persona))
             for otra_persona in personas if otra_persona != persona)
    lista = sorted(lista, key=lambda x: x[1], reverse=True)
    gemelo = lista[0][0]  # persona
    nombre_gemelo = gemelo.nombre
    return nombre_gemelo


def valor_característica(tag_identificador, persona):
    personaa = filter(lambda x: x.nombre == persona, personas)
    persona = next(personaa)
    caracteristicas = (persona.altura, persona.ojo, persona.pelo, persona.piel,
                       persona.nariz, persona.pie, persona.vello,
                       persona.guata, persona.vision)
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_identificador)
    return caracteristicas[indice]


def min2(tag_caracteristica):
    if tag_caracteristica == "GTC" or tag_caracteristica == "GGA" \
            or tag_caracteristica == "TCT" or tag_caracteristica == "GTA":
        menos_frecuente = caso1(tag_caracteristica, "min")
        return menos_frecuente
    elif tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        menos_frecuente = caso2(tag_caracteristica, "min")
        return menos_frecuente
    else:
        print("Esta caracteristica no es valida para esta consulta")


def max2(tag_caracteristica):
    if tag_caracteristica == "GTC" or tag_caracteristica == "GGA" \
            or tag_caracteristica == "TCT" or tag_caracteristica == "GTA":
        menos_frecuente = caso1(tag_caracteristica, "max")
        return menos_frecuente
    elif tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        menos_frecuente = caso2(tag_caracteristica, "max")
        return menos_frecuente
    else:
        print("Esta caracteristica no es valida para esta consulta")


def caso1(tag_caracteristica, tipo):
    # tipo es un string que dice si buscamos el maximo o el minimo
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_caracteristica) + 4
    frecuencias_particular = (persona[indice] for persona in personas)
    frecuencias_sistema = Counter(frecuencias_particular)
    #frecuencias_sistema = [(fenotipo, cantidad) for fenotipo, cantidad in
    #                       frecuencias_sistema.items()]
    #frecuencias_sistema.sort(key=lambda x: x[1])
    frecuencias_sistema = ((fenotipo, cantidad) for fenotipo, cantidad in
                            frecuencias_sistema.items())
    frecuencias_sistema = sorted(frecuencias_sistema, key=lambda x: x[1])
    if tipo == "min":
        return frecuencias_sistema[0][0]
    elif tipo == "max":
        return frecuencias_sistema[-1][0]


def caso2(tag_caracteristica, tipo):
    tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
    indice = tags.index(tag_caracteristica) + 4
    frecuencias_particular = (persona[indice] for persona in personas)
    if tipo == "min":
        return min(frecuencias_particular)
    elif tipo == "max":
        return max(frecuencias_particular)


def prom(tag_caracteristica):
    if tag_caracteristica == "AAG" or tag_caracteristica == "CTC":
        tags = ["AAG", "GTC", "GGA", "TCT", "GTA", "CTC", "CGA", "TGG", "TAG"]
        indice = tags.index(tag_caracteristica) + 4
        frecuencias_particular = (persona[indice] for persona in personas)
        suma = reduce(lambda x, y: x + y, frecuencias_particular)
        total = len(personas)
        promedio = suma / total
        return promedio


print(pariente_de("2", "Stephanie Chau"))

print(ascendencia("Stephanie Chau"))
print(ascendencia("Felipe Dominguez"))
print(ascendencia("Rick Sánchez"))
print(ascendencia("fringles inthestreet"))
print("ASCENDENCIAS")
for persona in personas:
    print(persona.nombre, ascendencia(persona.nombre))
print("")

print("INDICES")
for persona in personas:
    print(persona.nombre, índice_de_tamaño(persona.nombre))
print("")

#lista = [1, 2, 3, 1]
#lista2= [1, 4, 5]
#listaa = set(lista) & set(lista2)
#print(Counter(lista))

print(gemelo_genético("Jesús De Nazaret"))

print(valor_característica("TGG", "Stephanie Chau"))
print(min2("TCT"))
print(min2("CTC"))

print(max2("TCT"))
print(max2("CTC"))

print(prom("AAG"))

lista_consultas = [ascendencia, índice_de_tamaño, pariente_de, gemelo_genético,
             valor_característica, min2, max2, prom]
#print("a", lista_consultas[0].__name__)

gen = (i for i in range(10))

lista = [3, 2, 5]
a = sorted(gen, key=lambda elem: elem)
print(a)