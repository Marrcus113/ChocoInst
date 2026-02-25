from setuptools import setup, find_packages
import os

# Читаем длинное описание из README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="chocoinst",
    version="1.0.1",
    author="Марк",
    author_email="",
    description="🍫 ChocoInst - установка пакетов через Chocolatey с графическим интерфейсом",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Marrcus113/ChocoInst",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Microsoft :: Windows",
    ],
    python_requires=">=3.8",
    install_requires=[
        # Здесь можно добавить зависимости, если они есть
        # Например: "pyinstaller" не нужен, это для сборки, а не для работы
    ],
    entry_points={
        "console_scripts": [
            "chocoinst=main:main",  # если у тебя есть функция main() в main.py
        ],
    },
    include_package_data=True,
    package_data={
        "": ["icon.ico"],  # включаем иконку в пакет
    },
)
