# remote-types repository template

[![Tests](https://github.com/UCLM-ESI/remote-types/actions/workflows/tests.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/tests.yml)
[![Linters](https://github.com/UCLM-ESI/remote-types/actions/workflows/linters.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/linters.yml)
[![Type checking](https://github.com/UCLM-ESI/remote-types/actions/workflows/typechecking.yml/badge.svg)](https://github.com/UCLM-ESI/remote-types/actions/workflows/typechecking.yml)

Template for the SSDD laboratory 2024-2025

## Installation

To locally install the package, just run

```
pip install .
```

Or, if you want to modify it during your development,

```
pip install -e .
```

## Execution

To run the template server, just install the package and run

```
remotetypes --Ice.Config=config/remotetypes.config
```

## Configuration

This template only allows to configure the server endpoint. To do so, you need to modify
the file `config/remotetypes.config` and change the existing line.

For example, if you want to make your server to listen always in the same TCP port, your file
should look like

```
remotetypes.Endpoints=tcp -p 10000
```

## Running tests and linters locally

If you want to run the tests and/or linters, you need to install the dependencies for them:

- To install test dependencies: `pip install .[tests]`
- To install linters dependencies: `pip install .[linters]`

All the tests runners and linters are configured in the `pyproject.toml`.

## Continuous integration

This repository is already configured to run the following workflows:

- Ruff: checks the format, code style and docs style of the source code.
- Pylint: same as Ruff, but it evaluates the code. If the code is rated under a given threshold, it fails.
- MyPy: checks the types definitions and the usages, showing possible errors.
- Unit tests: uses `pytest` to run unit tests. The code coverage is quite low. Fixing the tests, checking the
    test coverage and improving it will make a difference.

If you create your repository from this template, you will get all those CI for free.

## Slice usage

The Slice file is provided inside the `remotetypes` directory. It is only loaded once when the `remotetypes`
package is loaded by Python. It makes your life much easier, as you don't need to load the Slice in every module
or submodule that you define.

The code loading the Slice is inside the `__init__.py` file.

# segunda entrega: Realización de un cliente con Kafka:
El programa cliente realizará mediante Apache Kafka una realización de ejercicios sobre las clases realizadas con .ice, remotedict.py, remotelist.py, remotedict.py.

Para ello necesitamos tener la version 3.8 de python o superior, Apache kafka, con un broker en ejecucion de localhost:9092 y las dependencias al realizar `pip install -e`.

## configuration

lo primero que se deberá hacer sera clonar el repositorio, con el siguiente comando `git clone <urlRepo>`.
Tras esto deberemos entrar a la carpeta con `cd <nombreCarpeta>`.

Tras esto activaremos el entorno virtual e instalaremos las dependencias.

Para iniciar el servidor utilizaremos kafka si no esta ya `kafka-server-start.sh /path/to/kafka/config/server.properties`, e iniciaremos el servidor con `remotetypes --Ice.Config=config/remotetypes.config` y en otra terminal, `sudo docker-compose up` tras esto iniciamos el cliente `python3 cliente.py`y realizamos el envio de los ejercicios a realizar, que son los siguientes:

remoteDict:

setItem: `echo '[{"id": 1, "object_type": "RDict", "object_identifier": "test_dict", "operation": "setItem", "args": {"key": "clave1", "item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

getItem: `echo '[{"id": 2, "object_type": "RDict", "object_identifier": "test_dict", "operation": "getItem", "args": {"key": "clave1"}}]' | kcat -P -b localhost:9092 -t operation`

remove : `echo '[{"id": 3, "object_type": "RDict", "object_identifier": "test_dict", "operation": "remove", "args": {"item": "clave1"}}]' | kcat -P -b localhost:9092 -t operation`

remotelist:

append: `echo '[{"id": 4, "object_type": "RList", "object_identifier": "test_list", "operation": "append", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

getItem: `echo '[{"id": 5, "object_type": "RList", "object_identifier": "test_list", "operation": "getItem", "args": {"index": 0}}]' | kcat -P -b localhost:9092 -t operation`

remove: `echo '[{"id": 6, "object_type": "RList", "object_identifier": "test_list", "operation": "remove", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

remoteSet:

add: `echo '[{"id": 7, "object_type": "RSet", "object_identifier": "test_set", "operation": "add", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

contains: `echo '[{"id": 8, "object_type": "RSet", "object_identifier": "test_set", "operation": "contains", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operation`

remove: `echo '[{"id": 9, "object_type": "RSet", "object_identifier": "test_set", "operation": "remove", "args": {"item": "valor1"}}]' | kcat -P -b localhost:9092 -t operations`

iterable:

`echo '[{"id": 10, "object_type": "RDict", "object_identifier": "test_dict", "operation": "iter"}]' | kcat -P -b localhost:9092 -t operation`

Tras esto para comprobar los resultados utilizaremos el siguiente comando:

`kcat -C -b localhost:9092 -t results -o beginning`