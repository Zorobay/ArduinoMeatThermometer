import math

type Number = int | float


def c_to_kelvin(c: float) -> float:
    return c + 273.15


def kelvin_to_c(k: float) -> float:
    return k - 273.15


def root(x: Number, n: int = 2) -> float:
    """
    Calculates the nth root of x.

    :param x: The number to take the root of
    :param n: The degree of the root (e.g. 2 for square root, 3 for cube root)
    :return: The nth root of x
    """
    return math.copysign(math.pow(abs(x), 1 / n), x)


def cube(x: Number) -> float:
    return math.pow(x, 3)


def square(x: Number) -> float:
    return math.pow(x, 2)


def _calc_L_steinhart_hart(Rn: Number) -> float:
    return math.log(Rn)


def _calc_Y_steinhart_hart(Tn: Number) -> float:
    return 1 / Tn


def calc_C_steinhart_hart(t_values: list[float], adc_values: list[int], Rfixed: int) -> float:
    r_values = [calc_Rtherm_voltage_divider(Rfixed, adc) for adc in adc_values]
    L1 = _calc_L_steinhart_hart(r_values[0])
    L2 = _calc_L_steinhart_hart(r_values[1])
    L3 = _calc_L_steinhart_hart(r_values[2])
    Y1 = _calc_Y_steinhart_hart(t_values[0])
    Y2 = _calc_Y_steinhart_hart(t_values[1])
    Y3 = _calc_Y_steinhart_hart(t_values[2])
    gamma2 = (Y2 - Y1) / (L2 - L1)
    gamma3 = (Y3 - Y1) / (L3 - L1)
    return (gamma3 - gamma2) / ((L3 - L2) * (L1 + L2 + L3))


def calc_B_steinhart_hart(C: float, t_values: list[float], adc_values: list[int], Rfixed: int) -> float:
    r_values = [calc_Rtherm_voltage_divider(Rfixed, adc) for adc in adc_values]
    L1 = _calc_L_steinhart_hart(r_values[0])
    L2 = _calc_L_steinhart_hart(r_values[1])
    Y1 = _calc_Y_steinhart_hart(t_values[0])
    Y2 = _calc_Y_steinhart_hart(t_values[1])
    gamma2 = (Y2 - Y1) / (L2 - L1)
    return gamma2 - C * (square(L1) + (L1 * L2) + square(L2))


def calc_A_steinhart_hart(B: float, C: float, t_values: list[float], adc_values: list[int], Rfixed: int) -> float:
    r_values = [calc_Rtherm_voltage_divider(Rfixed, adc) for adc in adc_values]
    L1 = _calc_L_steinhart_hart(r_values[0])
    Y1 = _calc_Y_steinhart_hart(t_values[0])
    return Y1 - L1 * (B + C * square(L1))


def calc_Rtherm_voltage_divider(Rfixed: int, ADCtherm: Number, ADCmax: int = 4095) -> float:
    return Rfixed * (ADCtherm / (ADCmax - ADCtherm))


def calc_ADCtherm_voltage_divider(Rtherm: float, Rfixed: int, ADCmax: int = 4095) -> float:
    return Rtherm * (ADCmax / (Rfixed + Rtherm))


def calc_steinhart_hart(R: Number, A: Number, B: Number, C: Number) -> float:
    return 1 / (A + B * math.log(R) + C * math.pow(math.log(R), 3))


## Resistance (R) is desired, temperature (T) is known
def calc_r_stenhart_hart(T: Number, A: Number, B: Number, C: Number) -> float:
    x = (A - 1 / T) / C
    y = root(cube(B / (3 * C)) + square(x) / 4)
    return math.exp(root(y - (x / 2), 3) - root(y + (x / 2), 3))


def calc_steinhart_hart_inverse_analytical(t_celcius: Number, A: Number, B: Number, C: Number) -> float:
    high, low = 25000, 10
    for _ in range(50):
        r_mid = (high + low) / 2
        t = kelvin_to_c(1 / (A + B * math.log(r_mid) + C * math.pow(math.log(r_mid), 3)))
        if t > t_celcius:
            low = r_mid
        else:
            high = r_mid
    return (high + low) / 2
