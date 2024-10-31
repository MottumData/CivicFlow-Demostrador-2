from setuptools import setup, find_packages

setup(
    name="Asistente Virtual de Codexca",
    version="0.0.1",
    description="Asistente Virtual para Codexca a través de LLM e interfaz creada con Streamlit",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Mottum, Arturo Ortiz",
    author_email="hello@mottum.io, a.ortiz@mottum.io",
    url="https://github.com/MottumData/VA-Codexca",
    packages=find_packages(),
    install_requires=[
        "streamlit==1.37.0",
        "streamlit-option-menu==0.3.13",
        "pandas==2.2.2",
        "numpy==1.26.4",
        "python-dotenv==1.0.1",
        "langchain~=0.2.12"
    ],
    python_requires='>=3.9',
)
