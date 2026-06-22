import argparse
import serial
import serial.tools.list_ports
import threading
import time
import sys

__version__ = "0.1.0"

def serial_reader(ser, stop_event, echo, log_file):
    while not stop_event.is_set():
        try:
            line = ser.readline()
            if line:
                text = line.decode(errors="ignore").strip()

                if text:
                    msg = f"RX: {text}"

                    print(f"\n{msg}")

                    if log_file:
                        log_file.write(msg + "\n")
                        log_file.flush()

                    if echo:
                        print("> ", end="", flush=True)

        except Exception:
            break


def list_ports():
    print("\nPuertos COM disponibles:\n")
    ports = serial.tools.list_ports.comports()

    if not ports:
        print("No se encontraron puertos.")
        return

    for p in ports:
        print(f" - {p.device} ({p.description})")

    print()


def parse_args():
    parser = argparse.ArgumentParser(
        prog="serial-com",
        description="Herramienta de diagnosticos COM"
    )

    parser.add_argument("--version", action="version", version=f"serial-com {__version__}")
    parser.add_argument("--port", type=str, help="Puerto COM (Ejemplo: COM3)")
    parser.add_argument("--baud", type=int, default=115200, help="Baud rate (Por defecto: 115200)")
    parser.add_argument("--timeout", type=float, default=0.1, help="Timeout de lectura")
    parser.add_argument("--list", action="store_true", help="Listar puertos COM y salir")
    parser.add_argument("--echo", action="store_true", help="mostrar TX/RX labels")
    parser.add_argument("--crlf", action="store_true", help="Usar CRLF en vez de LF")
    parser.add_argument("--log", type=str, help="Ruta de archivo log (TX + RX)")
    return parser.parse_args()


def main():
    args = parse_args()

    if args.list:
        list_ports()
        return

    if not args.port:
        print("ERROR: --port es requerido (o usa --list)")
        sys.exit(1)

    try:
        ser = serial.Serial(
            args.port,
            args.baud,
            timeout=args.timeout
        )
    except serial.SerialException as e:
        print(f"No se pudo abrir {args.port}: {e}")
        sys.exit(1)

    print(f"\nConectado a {args.port} @ {args.baud}")
    print("Escribe 'exit' o Ctrl+C para salir.\n")

    stop_event = threading.Event()

    log_file = None
    if args.log:
        log_file = open(args.log, "a", encoding="utf-8")

    thread = threading.Thread(
        target=serial_reader,
        args=(ser, stop_event, args.echo, log_file),
        daemon=True
    )
    thread.start()

    try:
        while True:
            msg = input("> ")

            if msg.lower() == "exit":
                break

            line_end = "\r\n" if args.crlf else "\n"
            data = (msg + line_end).encode()

            ser.write(data)

            if log_file:
                log_file.write(f"TX: {msg}\n")
                log_file.flush()

    except KeyboardInterrupt:
        print("\nCtrl+C detectado.")

    finally:
        stop_event.set()
        time.sleep(0.2)

        if ser.is_open:
            ser.close()

        if log_file:
            log_file.close()

        print("Puerto serial cerrado.")


if __name__ == "__main__":
    main()