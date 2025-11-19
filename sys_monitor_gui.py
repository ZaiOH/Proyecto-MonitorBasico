#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sys_monitor_gui.py
Monitor básico del sistema con interfaz gráfica (Tkinter).
Muestra métricas dinámicas (CPU y Memoria) actualizadas en tiempo real,
y otras métricas estáticas/actualizadas como procesos, disco y red.

Requisitos:
    pip install psutil matplotlib

Autor: Zaira Daniela Ortega Hernandez
Fecha: 2025-11-18
"""

import tkinter as tk
from tkinter import ttk
import psutil
import time
from collections import deque

# Intentar importar matplotlib para mostrar gráfico histórico de CPU.
# Si no está disponible, el programa sigue funcionando sin el gráfico.
try:
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    import matplotlib.figure as mplfig
    MATPLOTLIB_AVAILABLE = True
except Exception:
    MATPLOTLIB_AVAILABLE = False

# -------------------------
# CONFIGURACIÓN GLOBAL
# -------------------------
UPDATE_INTERVAL_MS = 1000  # Frecuencia de actualización en milisegundos (1000 ms = 1 s)
CPU_HISTORY_LEN = 60       # Número de valores históricos a guardar para el gráfico (ej. últimos 60 segundos)


# -------------------------
# CLASE: SystemMonitorApp
# -------------------------
class SystemMonitorApp:
    """
    Clase principal de la aplicación Tkinter que contiene:
    - Indicadores de CPU y memoria (barras y %).
    - Contadores de procesos, disco (lecturas/escrituras) y red (bytes).
    - Gráfico histórico de CPU (si matplotlib está instalado).
    """

    def __init__(self, root):
        """
        Inicializa la ventana principal y todos los widgets.
        """
        self.root = root
        root.title("Monitor básico del sistema")
        root.geometry("780x480")
        root.resizable(False, False)

        # Variables que usan los widgets para mostrar valores en tiempo real
        self.cpu_percent_var = tk.DoubleVar(value=0.0)
        self.mem_percent_var = tk.DoubleVar(value=0.0)
        self.proc_count_var = tk.IntVar(value=0)
        self.disk_read_var = tk.StringVar(value="0 B/s")
        self.disk_write_var = tk.StringVar(value="0 B/s")
        self.net_sent_var = tk.StringVar(value="0 B/s")
        self.net_recv_var = tk.StringVar(value="0 B/s")
        self.last_update_var = tk.StringVar(value="")

        # Histórico de CPU para el gráfico (deque es eficiente para pop/append)
        self.cpu_history = deque([0.0] * CPU_HISTORY_LEN, maxlen=CPU_HISTORY_LEN)
        self.prev_disk = psutil.disk_io_counters()
        self.prev_net = psutil.net_io_counters()
        self.prev_time = time.time()

        # Crear interfaz (frames + widgets)
        self._build_gui()

        # Iniciar loop de actualización periódica
        self._schedule_update()

    # ---------------------
    # Construcción GUI
    # ---------------------
    def _build_gui(self):
        """
        Construye los widgets: barras de progreso, labels, y (opcional) gráfico.
        """

        # Marco superior con métricas dinámicas
        top_frame = ttk.Frame(self.root, padding=(10, 10))
        top_frame.pack(side="top", fill="x")

        # CPU
        cpu_label = ttk.Label(top_frame, text="CPU (%)", font=("Segoe UI", 10, "bold"))
        cpu_label.grid(row=0, column=0, sticky="w")

        self.cpu_bar = ttk.Progressbar(top_frame, orient="horizontal", length=400,
                                       mode="determinate", maximum=100,
                                       variable=self.cpu_percent_var)
        self.cpu_bar.grid(row=0, column=1, padx=(8, 10), sticky="w")

        self.cpu_percent_lbl = ttk.Label(top_frame, textvariable=self.cpu_percent_var, width=6)
        self.cpu_percent_lbl.grid(row=0, column=2, sticky="w")

        # Memoria
        mem_label = ttk.Label(top_frame, text="Memoria (%)", font=("Segoe UI", 10, "bold"))
        mem_label.grid(row=1, column=0, pady=(8, 0), sticky="w")

        self.mem_bar = ttk.Progressbar(top_frame, orient="horizontal", length=400,
                                       mode="determinate", maximum=100,
                                       variable=self.mem_percent_var)
        self.mem_bar.grid(row=1, column=1, padx=(8, 10), pady=(8, 0), sticky="w")

        self.mem_percent_lbl = ttk.Label(top_frame, textvariable=self.mem_percent_var, width=6)
        self.mem_percent_lbl.grid(row=1, column=2, pady=(8, 0), sticky="w")

        # Info resumida (procesos, disco, red)
        right_frame = ttk.Frame(self.root, padding=(10, 10))
        right_frame.pack(side="top", fill="x")

        info_frame = ttk.Frame(right_frame)
        info_frame.pack(side="left", fill="both", expand=True)

        # Número de procesos
        proc_lbl_title = ttk.Label(info_frame, text="Procesos:", font=("Segoe UI", 9, "bold"))
        proc_lbl_title.grid(row=0, column=0, sticky="w")
        proc_lbl_val = ttk.Label(info_frame, textvariable=self.proc_count_var)
        proc_lbl_val.grid(row=0, column=1, sticky="w", padx=(5, 0))

        # Disco (lecturas/escrituras por segundo)
        disk_lbl_title = ttk.Label(info_frame, text="Disco (R/W):", font=("Segoe UI", 9, "bold"))
        disk_lbl_title.grid(row=1, column=0, sticky="w", pady=(6, 0))
        disk_lbl_val = ttk.Label(info_frame, textvariable=self.disk_read_var)
        disk_lbl_val.grid(row=1, column=1, sticky="w", padx=(5, 0))
        disk_lbl_val2 = ttk.Label(info_frame, textvariable=self.disk_write_var)
        disk_lbl_val2.grid(row=1, column=2, sticky="w", padx=(8, 0))

        # Red (enviado/recibido por segundo)
        net_lbl_title = ttk.Label(info_frame, text="Red (S/R):", font=("Segoe UI", 9, "bold"))
        net_lbl_title.grid(row=2, column=0, sticky="w", pady=(6, 0))
        net_lbl_val = ttk.Label(info_frame, textvariable=self.net_sent_var)
        net_lbl_val.grid(row=2, column=1, sticky="w", padx=(5, 0))
        net_lbl_val2 = ttk.Label(info_frame, textvariable=self.net_recv_var)
        net_lbl_val2.grid(row=2, column=2, sticky="w", padx=(8, 0))

        # Última actualización
        last_lbl = ttk.Label(info_frame, text="Última actualización:", font=("Segoe UI", 8))
        last_lbl.grid(row=3, column=0, sticky="w", pady=(8, 0))
        last_val = ttk.Label(info_frame, textvariable=self.last_update_var)
        last_val.grid(row=3, column=1, columnspan=2, sticky="w", pady=(8, 0))

        # Espacio para figura (gráfico histórico de CPU) si matplotlib está disponible
        if MATPLOTLIB_AVAILABLE:
            fig = mplfig.Figure(figsize=(8, 3), dpi=100)
            self.ax = fig.add_subplot(111)
            self.ax.set_title("Uso CPU (histórico)")
            self.ax.set_ylim(0, 100)
            self.ax.set_ylabel("% CPU")
            self.ax.set_xlabel("T (segundos)")
            self.line, = self.ax.plot(list(range(-CPU_HISTORY_LEN + 1, 1)), list(self.cpu_history))

            canvas = FigureCanvasTkAgg(fig, master=self.root)
            canvas.get_tk_widget().pack(side="bottom", fill="both", expand=False, padx=10, pady=8)
            self.canvas = canvas
        else:
            # Si no está matplotlib, mostramos una nota en la UI
            note = ttk.Label(self.root, text="(Gráfico de CPU deshabilitado: falta matplotlib)", foreground="gray")
            note.pack(side="bottom", pady=(16, 8))

    # ---------------------
    # Actualización de métricas
    # ---------------------
    def _collect_metrics(self):
        """
        Recopila métricas del sistema usando psutil:
        - cpu_percent: porcentaje de uso de CPU (promedio)
        - mem_percent: porcentaje de uso de memoria
        - proc_count: número de procesos
        - disk io: bytes leídos/escritos desde la última medición -> convertidos a B/s
        - net io: bytes enviados/recibidos desde la última medición -> convertidos a B/s
        """
        # Tiempo actual (para cálculo de delta)
        now = time.time()
        dt = now - self.prev_time if self.prev_time else 1.0
        self.prev_time = now

        # CPU y memoria (metricas dinámicas obligatorias)
        cpu = psutil.cpu_percent(interval=None)  # % desde la última llamada
        mem = psutil.virtual_memory().percent

        # Número de procesos
        proc_count = len(psutil.pids())

        # Disco IO (bytes totales desde boot). Convertimos a bytes por segundo (B/s)
        cur_disk = psutil.disk_io_counters()
        read_bytes = max(0, cur_disk.read_bytes - self.prev_disk.read_bytes)
        write_bytes = max(0, cur_disk.write_bytes - self.prev_disk.write_bytes)
        read_bps = read_bytes / dt
        write_bps = write_bytes / dt
        self.prev_disk = cur_disk

        # Red IO (bytes totales). Calculamos B/s similar a disco.
        cur_net = psutil.net_io_counters()
        sent_bytes = max(0, cur_net.bytes_sent - self.prev_net.bytes_sent)
        recv_bytes = max(0, cur_net.bytes_recv - self.prev_net.bytes_recv)
        sent_bps = sent_bytes / dt
        recv_bps = recv_bytes / dt
        self.prev_net = cur_net

        # Guardar histórico CPU
        self.cpu_history.append(cpu)

        return {
            "cpu": cpu,
            "mem": mem,
            "proc_count": proc_count,
            "read_bps": read_bps,
            "write_bps": write_bps,
            "sent_bps": sent_bps,
            "recv_bps": recv_bps,
            "timestamp": now
        }

    def _format_bytes(self, bps):
        """
        Formatea B/s en una representación legible: B/s, KB/s, MB/s.
        """
        if bps < 1024:
            return f"{bps:.0f} B/s"
        elif bps < 1024**2:
            return f"{bps/1024:.1f} KB/s"
        else:
            return f"{bps/(1024**2):.2f} MB/s"

    def _update_widgets(self, metrics):
        """
        Actualiza widgets con los nuevos valores leídos.
        """
        # Actualizar valores de las variables
        self.cpu_percent_var.set(round(metrics["cpu"], 1))
        self.mem_percent_var.set(round(metrics["mem"], 1))
        self.proc_count_var.set(metrics["proc_count"])
        self.disk_read_var.set(self._format_bytes(metrics["read_bps"]))
        self.disk_write_var.set(self._format_bytes(metrics["write_bps"]))
        self.net_sent_var.set(self._format_bytes(metrics["sent_bps"]))
        self.net_recv_var.set(self._format_bytes(metrics["recv_bps"]))
        self.last_update_var.set(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(metrics["timestamp"])))

        # Actualizar gráfico si está disponible
        if MATPLOTLIB_AVAILABLE:
            self.line.set_ydata(list(self.cpu_history))
            # xdata no cambia (ejes fijos), sólo refrescamos la figura
            self.canvas.draw_idle()

    # ---------------------
    # Planificador de actualizaciones
    # ---------------------
    def _schedule_update(self):
        """
        Programa la recolección de métricas y actualización de la interfaz.
        Usamos `after` para evitar hilos extra y mantener la UI receptiva.
        """
        try:
            metrics = self._collect_metrics()
            self._update_widgets(metrics)
        except Exception as e:
            # Capturamos errores de psutil u otros e imprimimos en consola
            print("Error recogiendo métricas:", e)

        # Re-lanzar la actualización después del intervalo especificado
        self.root.after(UPDATE_INTERVAL_MS, self._schedule_update)


# -------------------------
# EJECUCIÓN
# -------------------------
def main():
    root = tk.Tk()
    app = SystemMonitorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
