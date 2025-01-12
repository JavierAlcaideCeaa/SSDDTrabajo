import sys
import os
import Ice
slice_path = os.path.join(
    os.path.dirname(__file__),
    "remotetypes.ice",
)
Ice.loadSlice(slice_path)
import RemoteTypes as rt

def test_rdict(factory):
    print("\n--- Probando RDict ---")
    rdict = rt.RDictPrx.checkedCast(factory.get(rt.TypeName.RDict, "DICT1"))

    # 1.3 - Longitud inicial (debería ser 0)
    print("Longitud inicial:", rdict.length())  # 0

    # 1.8 y 1.10 - setItem y getItem
    rdict.setItem("clave1", "valor1")
    print("Item recuperado:", rdict.getItem("clave1"))  # valor1

    # 1.6 - Hash inicial
    initial_hash = rdict.hash()
    print("Hash inicial:", initial_hash)

    # 1.4 y 1.5 - contains
    print("Contiene 'clave1':", rdict.contains("clave1"))  # True
    print("Contiene 'clave2':", rdict.contains("clave2"))  # False

    # 1.9 - getItem lanza KeyError
    try:
        rdict.getItem("clave2")
    except rt.KeyError:
        print("Excepción KeyError capturada (clave no existe)")

    # 1.7 - Hash después de modificación
    rdict.setItem("clave2", "valor2")
    print("Hash modificado:", rdict.hash())

    # 1.12 - pop elimina y devuelve
    value = rdict.pop("clave1")
    print("Valor eliminado con pop:", value)
    print("Longitud tras pop:", rdict.length())

    # 1.1 - remove elimina
    rdict.remove("clave2")
    print("Longitud tras remove:", rdict.length())

    # 1.2 - remove lanza KeyError
    try:
        rdict.remove("clave3")
    except rt.KeyError:
        print("Excepción KeyError capturada en remove")
        
    #1.11 - pop lanza KeyError
    try:
        rdict.pop("clave3")
    except rt.KeyError:
        print("Excepción KeyError capturada en pop")

        
def test_rlist(factory):
    print("\n--- Probando RList ---")
    rlist = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, "LIST1"))

    # 2.3 - Longitud inicial
    print("Longitud inicial:", rlist.length())  # 0

    # 2.8 - append añade
    rlist.append("a")
    rlist.append("b")
    rlist.append("c")
    print("Longitud tras append:", rlist.length())  # 3

    # 2.12 - getItem devuelve y mantiene
    print("Elemento en posición 1:", rlist.getItem(1))  # b

    # 2.10 - pop elimina y devuelve por índice
    print("Elemento eliminado con pop(1):", rlist.pop(1))
    print("Longitud tras pop:", rlist.length())  # 2

    # 2.4 - contains devuelve Frue
    print("Contiene 'z':", rlist.contains("z"))  # False
    
    # 2.5 - contains devuelve True
    print("Contiene 'a':", rlist.contains("a"))  # True

    # 2.6 - Hash inicial
    initial_hash = rlist.hash()
    print("Hash inicial:", initial_hash)

    # 2.1 - remove elimina por valor
    rlist.remove("a")
    print("Longitud tras remove:", rlist.length())  # 1

    # 2.11 - pop lanza IndexError
    try:
        rlist.pop(7)
    except rt.IndexError:
        print("Excepción IndexError capturada")

    # 2.7 - Hash tras modificación
    print("Hash tras modificación:", rlist.hash())

def test_rset(factory):
    print("\n--- Probando RSet ---")
    rset = rt.RSetPrx.checkedCast(factory.get(rt.TypeName.RSet, "SET1"))

    # 3.3 - Longitud inicial
    print("Longitud inicial:", rset.length())  # 0

    # 3.8 - add añade elementos
    rset.add("x")
    rset.add("y")
    rset.add("o")
    print("Longitud tras add:", rset.length())  # 2

    # 3.4 y 3.5 - contains devuelve True/False
    print("Contiene 'x':", rset.contains("x"))  # True
    print("Contiene 'z':", rset.contains("z"))  # False

    # 3.6 - Hash inicial
    initial_hash = rset.hash()
    print("Hash inicial:", initial_hash)

    # 3.1 - remove elimina un valor
    rset.remove("x")
    print("Longitud tras remove:", rset.length())  # 1

    # 3.2 - remove lanza KeyError
    try:
        rset.remove("z")
    except rt.KeyError:
        print("Excepción KeyError capturada")

    # 3.9 - pop devuelve y elimina
    value = rset.pop()
    print("Elemento eliminado con pop:", value)
    print("Longitud tras pop:", rset.length())  # 0
    

    # 3.10 - pop lanza KeyError
    try:
        rset.pop()
    except rt.KeyError:
        print("Excepción KeyError capturada en pop")

def test_iterables(factory):
    print("\n--- Probando Iterables ---")
    rdict = rt.RDictPrx.checkedCast(factory.get(rt.TypeName.RDict, "DICT1"))
    rlist = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, "LIST1"))
    rset = rt.RSetPrx.checkedCast(factory.get(rt.TypeName.RSet, "SET1"))
    
    rlist2 = rt.RListPrx.checkedCast(factory.get(rt.TypeName.RList, "LIST2"))
    rlist2.append("1")
    rlist2.append("2")
    rlist2.append("3")
    iterable1 = rdict.iter()
    iterable2 = rlist.iter()
    iterable3 = rset.iter()

    # 4.1 - El proxy iterable es válido
    print("Proxy Iterable válido:", bool(iterable1))
    print("Proxy Iterable válido:", bool(iterable2))
    print("Proxy Iterable válido:", bool(iterable3))

    # 4.2 - Iterar sobre los elementos
    print("Diccionario -> ")
    try:
        while True:
            item = iterable1.next()
            print("Elemento iterado:", item)
    except rt.StopIteration:
        print("Iteración completa")
    print("lista -> ")
    try:
        while True:
            item = iterable2.next()
            print("Elemento iterado:", item)
    except rt.StopIteration:
        print("Iteración completa")
    print("COnjunto -> ")
    try:
        while True:
            item = iterable3.next()
            print("Elemento iterado:", item)
    except rt.StopIteration:
        print("Iteración completa")

    # 4.4 - Modificación provoca CancelIteration
    '''rlist.append("4")
    try:
        iterable.next()
    except rt.CancelIteration:
        print("Excepción CancelIteration capturada")'''

def main():
    with Ice.initialize(sys.argv) as communicator:
        proxy = communicator.stringToProxy("factory -t -e 1.1:tcp -h 127.0.0.1 -p 10000 -t 60000")
        factory = rt.FactoryPrx.checkedCast(proxy)
        if not factory:
            raise RuntimeError("Proxy inválido")

        print("Conectado al servidor.")
        test_rdict(factory)
        test_rlist(factory)
        test_rset(factory)
        test_iterables(factory)


if __name__ == "__main__":
    main()
