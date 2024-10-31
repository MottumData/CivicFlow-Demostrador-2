# VA-Codexca

## Descripción

Este repositorio contiene la implementación del asistente virtual para EMPRESA. La aplicación está desarrollada
completamente en Python, utilizando Streamlit tanto para la interfaz de usuario como para el backend.

> **Nota:** La versión de Python utilizada para el desarrollo de este proyecto es la 3.11

## Guía de Uso

Lo primero a tener en cuenta es la variable de entorno para usar la API key de OpenAI. Para ello, se debe crear un
archivo
`.env` en la raíz del proyecto con la siguiente estructura:

```shell
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXX # Sustituir por la API key de OpenAI
LANGCHAIN_API_KEY=XXXXXXXXXXXXXXXX
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_PROJECT="Your project name"
```

### Despliegue local :computer:

Para el despliegue en local, se debe instalar las dependencias del proyecto. Para ello, se puede utilizar el siguiente
comando:

```shell
pip install -r requirements.txt
```

Una vez instaladas correctamente todas las dependencias, se puede ejecutar la aplicación con el siguiente comando:

```shell
streamlit run app.py
```

A continuación, podrás acceder a la aplicación en tu navegador a través de la dirección `http://localhost:8501`.

### Despliegue con Docker :whale:

Para el despliegue con Docker, se debe construir la imagen con el siguiente comando:

```shell
docker-compose up --build
```

A continuación, podrás acceder a la aplicación en tu navegador a través de la dirección `http://localhost:8501`.

## Licencia

:gear: TBD

## Autores

- Arturo Ortiz.
- ... :construction_worker: ...