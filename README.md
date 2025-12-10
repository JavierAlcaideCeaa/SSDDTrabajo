# Plantilla de repositorio remote-types

Plantilla para el laboratorio de SSDD 2024-2025

## Instalación

Para instalar el paquete localmente, ejecuta:

```
pip install .
```

O, si deseas modificarlo durante el desarrollo:

```
pip install -e .
```

## Ejecución

Para ejecutar el servidor de la plantilla, instala el paquete y ejecuta:

```
remotetypes --Ice.Config=config/remotetypes.config
```

## Configuración

Esta plantilla solo permite configurar el endpoint del servidor. Para hacerlo, necesitas modificar el archivo `config/remotetypes.config` y cambiar la línea correspondiente.

Por ejemplo, si quieres que tu servidor escuche siempre en el mismo puerto TCP, tu archivo debería quedar así:

```
remotetypes.Endpoints=tcp -p 10000
```

## Ejecución de tests y linters localmente

Si quieres ejecutar los tests y/o linters, necesitas instalar sus dependencias:

- Para instalar dependencias de test: `pip install .[tests]`
- Para instalar dependencias de linters: `pip install .[linters]`

Todos los runners de tests y linters están configurados en el archivo `pyproject.toml`.

## Integración continua

Este repositorio está configurado para ejecutar los siguientes flujos de trabajo:

- Ruff: verifica el formateo, el estilo de código y el estilo de la documentación del código fuente.
- Pylint: realiza funciones similares a Ruff, pero además evalúa el código y falla si la puntuación está por debajo de un umbral definido.
- MyPy: revisa las definiciones de tipos y sus usos, mostrando posibles errores.
- Test unitarios: utiliza `pytest` para ejecutar tests unitarios. La cobertura de tests es inicialmente baja. Mejorarla marcará la diferencia.

Si creas tu repositorio a partir de esta plantilla, tendrás toda esta CI configurada desde el inicio.

## Uso de Slice

El archivo Slice se encuentra en el directorio `remotetypes`. Solo se carga una vez cuando el paquete `remotetypes` se importa en Python. Esto facilita el uso, ya que no es necesario cargar el archivo Slice en cada módulo o submódulo que definas.

El código que carga el Slice está en el archivo `__init__.py`.

# Segunda entrega: Realización de un cliente con Kafka

El programa cliente utiliza Apache Kafka para ejecutar operaciones sobre las clases realizadas con .ice: remotedict.py, remotelist.py, y remoteset.py.

Requisitos:

- Python versión 3.8 o superior
- Apache Kafka, con un broker en funcionamiento en localhost:9092
- Todas las dependencias instaladas ejecutando `pip install -e .`

## Configuración

1. Clona el repositorio con: `git clone <urlRepo>`
2. Entra en la carpeta del repositorio: `cd <nombreCarpeta>`
3. Activa el entorno virtual e instala las dependencias.

Para iniciar el servidor debes arrancar Kafka (si no está ejecutándose) con:  
`kafka-server-start.sh /ruta/a/kafka/config/server.properties`  
y arrancar el servidor con:  
`remotetypes --Ice.Config=config/remotetypes.config`

## Uso de las clases remotas

### remoteDict

- setItem:  
  `echo '[{"id": 1, "object_type": "RDict", "object_identifier": "test_dict", "operation": "setItem", "args": {"key": "clave1", "item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`
- getItem:  
  `echo '[{"id": 2, "object_type": "RDict", "object_identifier": "test_dict", "operation": "getItem", "args": {"key": "clave1"}}]' | kcat -P -b localhost:9092 -t operation`
- remove:  
  `echo '[{"id": 3, "object_type": "RDict", "object_identifier": "test_dict", "operation": "remove", "args": {"item": "clave1"}}]' | kcat -P -b localhost:9092 -t operation`

### remotelist

- append:  
  `echo '[{"id": 4, "object_type": "RList", "object_identifier": "test_list", "operation": "append", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`
- getItem:  
  `echo '[{"id": 5, "object_type": "RList", "object_identifier": "test_list", "operation": "getItem", "args": {"index": 0}}]' | kcat -P -b localhost:9092 -t operation`
- remove:  
  `echo '[{"id": 6, "object_type": "RList", "object_identifier": "test_list", "operation": "remove", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

### remoteSet

- add:  
  `echo '[{"id": 7, "object_type": "RSet", "object_identifier": "test_set", "operation": "add", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`
- contains:  
  `echo '[{"id": 8, "object_type": "RSet", "object_identifier": "test_set", "operation": "contains", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`
- remove:  
  `echo '[{"id": 9, "object_type": "RSet", "object_identifier": "test_set", "operation": "remove", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

### iterable

`echo '[{"id": 10, "object_type": "RDict", "object_identifier": "test_dict", "operation": "iter"}]' | kcat -P -b localhost:9092 -t operation`

Para comprobar los resultados utiliza:

`kcat -C -b localhost:9092 -t results -o beginning`ando:

`kcat -C -b localhost:9092 -t results -o beginning`
