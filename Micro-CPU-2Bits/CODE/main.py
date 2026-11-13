# ==============================================================================
# Proyecto : Micro-CPU 2Bits - Calculadora de un dígito (0-3) con Ciclo de Instrucción
# Placa    : RP2040 Zero            Lenguaje: MicroPython
# Curso    : Arquitectura del Computador I - UPANA
#
# Qué simula:
#   - Ciclo de instrucción (LEDs): Fetch -> Decode -> Fetch -> Execute -> Write-Back
#   - Banderas de estado: Zero y Negative (LEDs) y Overflow (LED RGB integrado)
#   - Calculadora de 2 bits: operandos 0-3, operaciones + y -
# ==============================================================================

import machine
import utime
import neopixel

# --- 1. Asignación de pines GPIO (ver DOCUMENTATION/PINOUT_FINAL.md) ----------
# Botones: entradas con Pull-Up interna (botón presionado = 0 V)
BUTTON_PINS = {0: 0, 1: 1, 2: 2, 3: 3, '+': 4, '-': 5, '=': 6}

# LEDs del ciclo de instrucción y de banderas
PIN_LED_FETCH = 7
PIN_LED_DECODE = 8
PIN_LED_EXECUTE = 9
PIN_LED_WRITEBACK = 10
PIN_LED_ZERO = 11
PIN_LED_NEGATIVE = 12

# LED RGB integrado (NeoPixel) -> bandera Overflow
PIN_NEOPIXEL = 16

# Display de 7 segmentos (cátodo común), en orden a, b, c, d, e, f, g
SEGMENT_PINS = (13, 14, 15, 26, 27, 28, 29)

# --- 2. Constantes -------------------------------------------------------------
MAX_VALUE = 3            # Rango de la calculadora de 2 bits: 0 a 3
DEBOUNCE_MS = 30         # Tiempo de antirrebote
STEP_MS = 500            # Duración de las fases Fetch y Decode
PHASE_MS = 2000          # Duración de las fases Execute y Write-Back
# Color del LED de Overflow. El orden de colores depende del firmware: si en tu
# placa no se ve rojo, cambia a (255, 0, 0).
OVERFLOW_COLOR = (0, 255, 0)

# Segmentos encendidos para cada dígito (1 = encendido). None = display apagado.
#                a  b  c  d  e  f  g
DIGIT_SEGMENTS = {
    0: (1, 1, 1, 1, 1, 1, 0),
    1: (0, 1, 1, 0, 0, 0, 0),
    2: (1, 1, 0, 1, 1, 0, 1),
    3: (1, 1, 1, 1, 0, 0, 1),
    None: (0, 0, 0, 0, 0, 0, 0),
}

# --- 3. Inicialización del hardware --------------------------------------------
buttons = {name: machine.Pin(pin, machine.Pin.IN, machine.Pin.PULL_UP)
           for name, pin in BUTTON_PINS.items()}

led_fetch = machine.Pin(PIN_LED_FETCH, machine.Pin.OUT)
led_decode = machine.Pin(PIN_LED_DECODE, machine.Pin.OUT)
led_execute = machine.Pin(PIN_LED_EXECUTE, machine.Pin.OUT)
led_writeback = machine.Pin(PIN_LED_WRITEBACK, machine.Pin.OUT)
led_zero = machine.Pin(PIN_LED_ZERO, machine.Pin.OUT)
led_negative = machine.Pin(PIN_LED_NEGATIVE, machine.Pin.OUT)

segment_pins = [machine.Pin(pin, machine.Pin.OUT) for pin in SEGMENT_PINS]
neopixel_led = neopixel.NeoPixel(machine.Pin(PIN_NEOPIXEL), 1)


# --- 4. Funciones de salida ----------------------------------------------------
def set_overflow_led(state):
    """Enciende (True) o apaga (False) el LED RGB integrado: bandera Overflow."""
    neopixel_led[0] = OVERFLOW_COLOR if state else (0, 0, 0)
    neopixel_led.write()


def display_digit(digit):
    """Muestra un dígito (0-3) en el display de 7 segmentos; None lo apaga."""
    for pin, on in zip(segment_pins, DIGIT_SEGMENTS[digit]):
        pin.value(on)


def clear_all_outputs():
    """Apaga todos los LEDs, el LED Overflow y el display."""
    for led in (led_fetch, led_decode, led_execute, led_writeback,
                led_zero, led_negative):
        led.value(0)
    set_overflow_led(False)
    display_digit(None)


# --- 5. Funciones de entrada ---------------------------------------------------
def read_button():
    """Devuelve el botón presionado (0-3, '+', '-', '=') o None si no hay ninguno."""
    for name, pin in buttons.items():
        if pin.value() == 0:      # Pull-Up: presionado = 0
            return name
    return None


def wait_for_press():
    """
    Espera una pulsación válida y devuelve el botón.
    Aplica antirrebote y espera a que el botón se suelte, para que una pulsación
    larga no se cuente dos veces.
    """
    while True:
        name = read_button()
        if name is not None:
            utime.sleep_ms(DEBOUNCE_MS)
            if read_button() == name:          # Sigue presionado: es válido
                while read_button() is not None:
                    utime.sleep_ms(10)         # Esperar a que se suelte
                return name
        utime.sleep_ms(10)


# --- 6. Fases del ciclo de instrucción -----------------------------------------
def fetch_operand(value):
    """FETCH: lee un operando, lo muestra en el display y enciende el LED Fetch."""
    led_fetch.value(1)
    display_digit(value)
    print("FETCH   -> operando:", value)
    utime.sleep_ms(STEP_MS)
    led_fetch.value(0)


def decode_operation(operation):
    """DECODE: identifica la operación (+ o -) y enciende el LED Decode."""
    led_decode.value(1)
    print("DECODE  -> operación:", operation)
    utime.sleep_ms(STEP_MS)
    led_decode.value(0)


def execute(operand1, operation, operand2):
    """
    EXECUTE (ALU): realiza la operación y actualiza las banderas.
    - Zero     : resultado == 0
    - Negative : resultado < 0
    - Overflow : resultado fuera del rango 0-3 (LED RGB integrado)
    """
    led_execute.value(1)
    if operation == '+':
        result = operand1 + operand2
    else:
        result = operand1 - operand2

    led_zero.value(result == 0)
    led_negative.value(result < 0)
    set_overflow_led(not 0 <= result <= MAX_VALUE)

    print("EXECUTE -> {} {} {} = {}".format(operand1, operation, operand2, result))
    utime.sleep_ms(PHASE_MS)
    led_execute.value(0)
    return result


def write_back(result):
    """WRITE-BACK: muestra el resultado; si está fuera de rango apaga el display."""
    led_writeback.value(1)
    display_digit(result if 0 <= result <= MAX_VALUE else None)
    print("WRITE-BACK -> resultado mostrado")
    utime.sleep_ms(PHASE_MS)
    led_writeback.value(0)


# --- 7. Máquina de estados -----------------------------------------------------
STATE_INPUT1, STATE_OPERATION, STATE_INPUT2, STATE_CALCULATE, STATE_RESULT = range(5)


def reset_calculator():
    """Apaga todo y deja la calculadora lista para un nuevo cálculo."""
    clear_all_outputs()
    print("Esperando el primer operando (0-3).")
    return STATE_INPUT1


print("Micro-CPU 2Bits iniciada.")
state = reset_calculator()
operand1 = operation = operand2 = result = None

while True:
    key = wait_for_press()
    is_digit = isinstance(key, int)       # Los únicos botones int son 0-3

    if state == STATE_INPUT1 and is_digit:
        operand1 = key
        fetch_operand(operand1)
        state = STATE_OPERATION

    elif state == STATE_OPERATION and key in ('+', '-'):
        operation = key
        decode_operation(operation)
        state = STATE_INPUT2

    elif state == STATE_INPUT2 and is_digit:
        operand2 = key
        fetch_operand(operand2)
        state = STATE_CALCULATE

    elif state == STATE_CALCULATE and key == '=':
        result = execute(operand1, operation, operand2)
        write_back(result)
        state = STATE_RESULT

    elif state == STATE_RESULT and key == '=':
        print("Reiniciando...")
        state = reset_calculator()
