# COMPONENTES — Micro-CPU 2Bits

Listado de materiales usados en el proyecto, con cantidad, tipo y especificaciones clave.

## Hardware

| # | Componente | Cantidad | Especificación | Función en el proyecto |
|---|---|---|---|---|
| 1 | Placa RP2040 Zero | 1 | Waveshare, USB-C, soporte para MicroPython | Microcontrolador: ejecuta la lógica y controla entradas y salidas |
| 2 | Pulsadores | 7 | 4 para dígitos (0-3) y 3 para operaciones (+, −, =) | Entradas de la calculadora |
| 3 | LEDs monocromáticos | 6 | Ver colores en la tabla de abajo | Ciclo de instrucción (4) y banderas Zero/Negative (2) |
| 4 | Resistencias | <!-- COMPLETAR: 6 o 7 --> | 220 Ω | Limitar la corriente de los LEDs |
| 5 | Display de 7 segmentos | 1 | **Cátodo común** | Mostrar los operandos y el resultado (0-3) |
| 6 | Protoboard | <!-- COMPLETAR: cantidad usada --> | — | Montaje del circuito |
| 7 | Cable para protoboard o UTP | 1 | — | Conexiones entre la placa, el display y los LEDs |
| 8 | Jumpers hembra-macho | 5 | — | Conexiones auxiliares |
| 9 | Cable USB-C | 1 | Datos y alimentación | Alimentación de la placa y carga del código |

<!-- COMPLETAR: si agregaste una resistencia en el COM del display, cuéntala en la fila 4 y
     menciónala en PINOUT_FINAL.md. -->

**Componente integrado en la placa (no se cuenta aparte):** LED RGB NeoPixel en el GPIO 16, usado como bandera **Overflow**.

## LEDs usados

Colores según el prototipo armado:

| LED | Función | Color |
|---|---|---|
| FETCH | Fase Fetch | Verde |
| DECODE | Fase Decode | Azul |
| EXECUTE | Fase Execute | Rojo |
| WRITE-BACK | Fase Write-Back | Azul |
| ZERO | Bandera Zero | Blanco |
| NEGATIVE | Bandera Negative | Rojo |

<!-- COMPLETAR: confirma estos colores con tu prototipo final. El diagrama de Cirkit Designer
     usa otros colores; si lo actualizas para que coincida, no cambia nada aquí. -->

## Software y herramientas

| Herramienta | Uso |
|---|---|
| MicroPython | Lenguaje de programación de la placa |
| Thonny | IDE para cargar y ejecutar el código |
| Cirkit Designer | Diagrama del circuito (`HARDWARE/Diagrama_Circuito.png`) |
| GitHub | Repositorio y documentación |

## Referencias

- Conexión de cada componente: [`PINOUT_FINAL.md`](PINOUT_FINAL.md)
- Descripción y uso del proyecto: [`../README.md`](../README.md)
