# serial-com
![Python](https://img.shields.io/badge/python-3.11+-blue)
![Platform](https://img.shields.io/badge/platform-windows-lightgrey)
![License](https://img.shields.io/badge/license-MIT-green)

Herramienta CLI ligera para diagnóstico y comunicación por puerto serial, orientada a equipos de campo como GNSS, dispositivos embebidos y equipos de topografía.

## ![Descargar](https://github.com/schweineorgel/serial-com/releases/download/v0.1.0/serial-com.exe)

## Características

- Listado de puertos COM disponibles
- Terminal interactiva (TX/RX en tiempo real)
- Configuración de baudrate
- Soporte CRLF / LF
- Recepción (RX) no bloqueante
- Logging opcional de sesión
- Binario ejecutable para Windows vía GitHub Actions

## Instalación

### Desde código fuente

```bash
git clone https://github.com/schweineorgel/serial-com.git
cd serial-com

python -m venv venv
venv\Scripts\activate   # Windows
source venv/bin/activate  # Linux/Mac

pip install -r requirements.txt
```

### Dependencias

```
pyserial
```

### Ejemplo de uso

```bash
serial-com --list
serial-com --port COM11 --baud 115200 --echo --log test.txt
```

### Flags

| Flag        | Descripción                                |
| ----------- | ------------------------------------------ |
| `--port`    | Puerto COM (ej: COM3)                      |
| `--baud`    | Velocidad de transmisión (default: 115200) |
| `--list`    | Lista puertos disponibles                  |
| `--echo`    | Muestra TX/RX en pantalla                  |
| `--crlf`    | Usa CRLF en lugar de LF                    |
| `--log`     | Guarda la sesión en archivo                |
| `--version` | Muestra versión del programa               |
