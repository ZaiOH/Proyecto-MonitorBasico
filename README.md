# Proyecto-MonitorBasico
El presente proyecto propone el desarrollo de un monitor básico del sistema capaz de mostrar en tiempo real información relevante sobre: 

* Uso de **CPU**
* Uso de **memoria RAM**
* Número de **procesos activos**
* Actividad de **disco**
* Actividad de **red**

El objetivo es comprender cómo un sistema operativo expone información interna y cómo obtenerla desde Python utilizando librerías adecuadas.

---

##  Características

✔ Interfaz gráfica con **Tkinter**

✔ Actualización en tiempo real (cada 1 segundo)

✔ Obtención de métricas usando **psutil**

✔ Uso multiplataforma (Windows, Linux, macOS)

✔ Código simple y documentado para fines educativos

---

##  Instalación 

1. Clona este repositorio:

```bash
git clone https://github.com/tu_usuario/Proyecto-MonitorBasico.git
cd Proyecto-MonitorBasico
```

2. Instala las dependencias:

```bash
pip install -r requirements.txt
```

 **Nota para Linux:**
Si Tkinter no está instalado:

```bash
sudo apt install python3-tk
```

---

## ▶ Ejecución

Ejecuta directamente el archivo principal:

```bash
python sys_monitor_gui.py
```

---

##  Estructura del Proyecto

```
Proyecto-MonitorBasico/
│── sys_monitor_gui.py
│── README.md
│── requirements.txt
|── LICENSE
```

---

##  Tecnologías utilizadas

| Tecnología   | Uso en el proyecto                        |
| ------------ | ----------------------------------------- |
| **Python 3** | Lenguaje principal                        |
| **psutil**   | Lectura de CPU, RAM, procesos, disco, red |
| **Tkinter**  | Interfaz gráfica básica                   |
| **time**     | Control del intervalo de actualización    |

---

##      Resumen

Un sistema operativo administra recursos como CPU, memoria y almacenamiento. Herramientas como **psutil** permiten acceder a estas métricas mediante una API de alto nivel.
Tkinter facilita la creación de interfaces gráficas simples, lo que permite visualizar estos datos dinámicamente.

---

##  Resultados esperados

El programa muestra una ventana con:

* Barra de uso de CPU
* Barra de uso de memoria
* Número de procesos activos
* Lecturas/escrituras de disco
* Envío/recepción de red

Actualizándose cada segundo.

---

##  Referencias (formato APA 6)

Python Software Foundation. (2024). *psutil Documentation (Version 5.9.8)*.
[https://psutil.readthedocs.io](https://psutil.readthedocs.io)

TkDocs. (2024). *Tkinter 8.6 Reference Guide*.
[https://tkdocs.com/tutorial/](https://tkdocs.com/tutorial/)

Tanenbaum, A. S., & Bos, H. (2023). *Modern Operating Systems* (5th ed.). Pearson.

---

##  Autor

* **Zaira Daniela Ortega Hernández**

