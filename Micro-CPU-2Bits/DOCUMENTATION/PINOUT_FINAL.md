# PINOUT_FINAL — Micro-CPU 2Bits

Lista de todos los pines GPIO usados en la **RP2040 Zero** y el componente al que están conectados.
Los números corresponden a las etiquetas **GPIO** de la placa (no a la posición física del pin) y coinciden con las constantes de `CODE/main.py`.

## Resumen rápido

| GPIO | Componente | Tipo |
|---|---|---|
| 0 | Botón `0` | Entrada (Pull-Up interna) |
| 1 | Botón `1` | Entrada (Pull-Up interna) |
| 2 | Botón `2` | Entrada (Pull-Up interna) |
| 3 | Botón `3` | Entrada (Pull-Up interna) |
| 4 | Botón `+` | Entrada (Pull-Up interna) |
| 5 | Botón `-` | Entrada (Pull-Up interna) |
| 6 | Botón `=` | Entrada (Pull-Up interna) |
| 7 | LED FETCH | Salida |
| 8 | LED DECODE | Salida |
| 9 | LED EXECUTE | Salida |
| 10 | LED WRITE-BACK | Salida |
| 11 | LED ZERO (bandera) | Salida |
| 12 | LED NEGATIVE (bandera) | Salida |
| 13 | Display 7 seg — segmento **a** | Salida |
| 14 | Display 7 seg — segmento **b** | Salida |
| 15 | Display 7 seg — segmento **c** | Salida |
| 26 | Display 7 seg — segmento **d** | Salida |
| 27 | Display 7 seg — segmento **e** | Salida |
| 28 | Display 7 seg — segmento **f** | Salida |
| 29 | Display 7 seg — segmento **g** | Salida |
| 16 | LED RGB integrado (NeoPixel) — bandera **OVERFLOW** | Salida (ya viene en la placa) |

## Detalle por grupo

### Botones (GPIO 0-6)

- Cada botón une su GPIO con **GND**.
- Se configuran con `Pin.PULL_UP` interna, por lo que **no necesitan resistencia externa**.
- Lógica: reposo = `1`, presionado = `0`.

| GPIO | Botón | Función |
|---|---|---|
| 0 | `0` | Dígito 0 |
| 1 | `1` | Dígito 1 |
| 2 | `2` | Dígito 2 |
| 3 | `3` | Dígito 3 |
| 4 | `+` | Operación suma |
| 5 | `-` | Operación resta |
| 6 | `=` | Ejecutar cálculo / reiniciar |

### LEDs del ciclo de instrucción y banderas (GPIO 7-12)

- Cada LED se conecta: **GPIO → resistencia de 220 Ω → ánodo (+) → cátodo (−) → GND**.
- Lógica: `1` = encendido, `0` = apagado.

| GPIO | LED | Se enciende cuando |
|---|---|---|
| 7 | FETCH | Se lee un operando |
| 8 | DECODE | Se lee la operación (+ o −) |
| 9 | EXECUTE | La ALU calcula (al presionar `=`) |
| 10 | WRITE-BACK | Se muestra el resultado |
| 11 | ZERO | El resultado es 0 |
| 12 | NEGATIVE | El resultado es menor que 0 |

### Display de 7 segmentos — cátodo común (GPIO 13, 14, 15, 26, 27, 28, 29)

- El pin **COM** va a **GND** (cátodo común: un `1` enciende el segmento).
- Cada segmento se conecta directamente a su GPIO.

<!-- COMPLETAR: si agregaste una resistencia entre el COM del display y GND, indícalo aquí
     (por ejemplo: "COM → resistencia de 220 Ω → GND"). -->

| GPIO | Segmento |
|---|---|
| 13 | a |
| 14 | b |
| 15 | c |
| 26 | d |
| 27 | e |
| 28 | f |
| 29 | g |

Segmentos encendidos por dígito (1 = encendido):

| Dígito | a | b | c | d | e | f | g |
|---|---|---|---|---|---|---|---|
| 0 | 1 | 1 | 1 | 1 | 1 | 1 | 0 |
| 1 | 0 | 1 | 1 | 0 | 0 | 0 | 0 |
| 2 | 1 | 1 | 0 | 1 | 1 | 0 | 1 |
| 3 | 1 | 1 | 1 | 1 | 0 | 0 | 1 |
| apagado | 0 | 0 | 0 | 0 | 0 | 0 | 0 |

### LED RGB integrado — bandera Overflow (GPIO 16)

- Es el NeoPixel que ya trae la RP2040 Zero; **no requiere cableado externo**.
- Se controla con la librería `neopixel` (1 LED en el GPIO 16).
- Se enciende cuando el resultado queda fuera del rango 0-3 (por ejemplo `2 + 2 = 4` o `1 - 2 = -1`).

## Alimentación

- La placa se alimenta y se programa por el cable **USB-C** (5 V).
- Todos los retornos (botones, cátodos de los LEDs y COM del display) se unen a un **GND común**.

## Verificación rápida (depuración)

| Síntoma | Qué revisar |
|---|---|
| Un botón no responde | Que un extremo esté en el GPIO indicado y el otro en GND |
| Un LED no enciende | Polaridad del LED, resistencia en serie y GPIO de la tabla |
| Segmento incorrecto en el display | Que el segmento (a-g) esté en el GPIO que corresponde |
| No se ve la bandera Overflow | El LED integrado está en el GPIO 16; revisar el color configurado en `OVERFLOW_COLOR` |
