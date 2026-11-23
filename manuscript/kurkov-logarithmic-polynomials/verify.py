import json
from fractions import Fraction
from functools import lru_cache
from math import comb, factorial


def add(*polynomials):
    result = {}
    for polynomial in polynomials:
        for monomial, coefficient in polynomial.items():
            result[monomial] = result.get(monomial, 0) + coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def scale(polynomial, scalar):
    return {monomial: scalar * coefficient for monomial, coefficient in polynomial.items() if scalar * coefficient}


def multiply(left, right):
    result = {}
    for left_monomial, left_coefficient in left.items():
        for right_monomial, right_coefficient in right.items():
            monomial = tuple(sorted(left_monomial + right_monomial))
            result[monomial] = result.get(monomial, 0) + left_coefficient * right_coefficient
    return {monomial: coefficient for monomial, coefficient in result.items() if coefficient}


def variable(index):
    return {(index,): Fraction(1)}


@lru_cache(None)
def recurrence(row, column):
    if row == 1:
        return variable(column)
    terms = [recurrence(row - 1, column + 1)]
    for index in range(1, row):
        terms.append(scale(multiply(recurrence(index, column), recurrence(row - index, 1)), -comb(row - 2, index - 1)))
    return add(*terms)


def source_series(order):
    return [{(): Fraction(1)}] + [scale(variable(index), Fraction(1, factorial(index))) for index in range(1, order + 1)]


def series_product(left, right, order):
    return [add(*(multiply(left[index], right[degree - index]) for index in range(degree + 1))) for degree in range(order + 1)]


def inverse_series(source):
    inverse = [{(): Fraction(1)}]
    for degree in range(1, len(source)):
        inverse.append(scale(add(*(multiply(source[index], inverse[degree - index]) for index in range(1, degree + 1))), -1))
    return inverse


def log_series(source):
    order = len(source) - 1
    increment = [{}] + source[1:]
    power = [{(): Fraction(1)}] + [{} for degree in range(order)]
    result = [{} for degree in range(order + 1)]
    for exponent in range(1, order + 1):
        power = series_product(power, increment, order)
        for degree in range(order + 1):
            result[degree] = add(result[degree], scale(power[degree], Fraction((-1) ** (exponent - 1), exponent)))
    return result


def exponential_series(increment):
    order = len(increment) - 1
    power = [{(): Fraction(1)}] + [{} for degree in range(order)]
    result = [dict(polynomial) for polynomial in power]
    for exponent in range(1, order + 1):
        power = series_product(power, increment, order)
        for degree in range(order + 1):
            result[degree] = add(result[degree], scale(power[degree], Fraction(1, factorial(exponent))))
    return result


def substitute(polynomial, replacements):
    terms = []
    for monomial, coefficient in polynomial.items():
        term = {(): coefficient}
        for index in monomial:
            term = multiply(term, replacements[index])
        terms.append(term)
    return add(*terms)


def polynomial_power(polynomial, exponent):
    result = {(): Fraction(1)}
    for step in range(exponent):
        result = multiply(result, polynomial)
    return result


def partitions(total, minimum=1):
    if total == 0:
        yield ()
    for first in range(minimum, total + 1):
        for tail in partitions(total - first, first):
            yield (first,) + tail


def coefficient_formula(degree):
    result = {}
    for monomial in partitions(degree):
        denominator = 1
        for index in set(monomial):
            multiplicity = monomial.count(index)
            denominator *= factorial(multiplicity) * factorial(index) ** multiplicity
        result[monomial] = Fraction((-1) ** (len(monomial) - 1) * factorial(len(monomial) - 1) * factorial(degree), denominator)
    return result


def appell(degree):
    return add(*({tuple([0] * exponent) + (() if degree == exponent else (degree - exponent,)): Fraction(comb(degree, exponent))} for exponent in range(degree + 1)))


def stirling_second(degree, blocks):
    values = [[0] * (degree + 1) for index in range(degree + 1)]
    values[0][0] = 1
    for size in range(1, degree + 1):
        for count in range(1, size + 1):
            values[size][count] = values[size - 1][count - 1] + count * values[size - 1][count]
    return values[degree][blocks]


@lru_cache(None)
def eulerian(degree, descents):
    if degree == 0:
        return int(descents == 0)
    if descents < 0 or descents >= degree:
        return 0
    return (degree - descents) * eulerian(degree - 1, descents - 1) + (descents + 1) * eulerian(degree - 1, descents)


def main():
    maximum_row = 10
    maximum_column = 6
    source = source_series(maximum_row)
    inverse = inverse_series(source)
    logarithm = log_series(source)
    quotient_cases = 0
    row_counts = []
    flattened = []
    for row in range(1, maximum_row + 1):
        polynomial = recurrence(row, 1)
        assert polynomial == scale(logarithm[row], factorial(row)) == coefficient_formula(row)
        assert all(coefficient.denominator == 1 for coefficient in polynomial.values())
        assert sum(polynomial.values()) == (1 if row == 1 else 0)
        row_counts.append(len(polynomial))
        reduced = {}
        for monomial, coefficient in polynomial.items():
            reduced[len(monomial)] = reduced.get(len(monomial), 0) + coefficient
        assert reduced == {blocks: Fraction((-1) ** (blocks - 1) * factorial(blocks - 1) * stirling_second(row, blocks)) for blocks in range(1, row + 1)}
        for column in range(1, maximum_column + 1):
            quotient = add(*(multiply(scale(variable(index + column), Fraction(1, factorial(index))), inverse[row - 1 - index]) for index in range(row)))
            assert recurrence(row, column) == scale(quotient, factorial(row - 1))
            quotient_cases += 1
        if row <= 7:
            monomials = sorted(polynomial, key=lambda monomial: (len(monomial), tuple(monomial.count(index) for index in range(1, row + 1))), reverse=True)
            flattened.extend(int(polynomial[monomial]) for monomial in monomials)
    expected_oeis = [1, -1, 1, 2, -3, 1, -6, 12, -4, -3, 1, 24, -60, 20, 30, -5, -10, 1, -120, 360, -120, -270, 30, 120, 30, -6, -15, -10, 1, 720, -2520, 840, 2520, -210, -1260, -630, 42, 210, 140, 210, -7, -21, -35, 1]
    assert flattened == expected_oeis
    for degree in range(maximum_row):
        moment = add(*(scale(multiply(recurrence(index + 1, 1), {(): Fraction(1)} if degree == index else variable(degree - index)), comb(degree, index)) for index in range(degree + 1)))
        assert moment == variable(degree + 1)
        right = add(multiply(variable(0), appell(degree)), *(scale(multiply(recurrence(index + 1, 1), appell(degree - index)), comb(degree, index)) for index in range(degree + 1)))
        assert right == appell(degree + 1)
        specialized = {}
        for monomial, coefficient in recurrence(degree + 1, 1).items():
            exponent = sum(index - 1 for index in monomial)
            specialized[exponent] = specialized.get(exponent, 0) + coefficient
        specialized = {exponent: coefficient for exponent, coefficient in specialized.items() if coefficient}
        transformed_eulerian = {}
        for exponent in range(degree + 1):
            coefficient = (-1) ** (degree + exponent) * sum(eulerian(degree, descents) * comb(degree - descents, exponent) for descents in range(degree - exponent + 1))
            if coefficient:
                transformed_eulerian[exponent] = coefficient
        assert specialized == transformed_eulerian
    family_order = 7
    for family in ['cycle', 'bell', 'lah']:
        factors = {index: factorial(index - 1) if family == 'cycle' else factorial(index) if family == 'lah' else 1 for index in range(1, family_order + 1)}
        exponent_series = [{}] + [scale(variable(index), Fraction(factors[index], factorial(index))) for index in range(1, family_order + 1)]
        family_series = exponential_series(exponent_series)
        replacements = {index: scale(family_series[index], factorial(index)) for index in range(1, family_order + 1)}
        for degree in range(1, family_order + 1):
            assert substitute(recurrence(degree, 1), replacements) == scale(variable(degree), factors[degree])
    replacements = {index: {(): Fraction(1 - index)} for index in range(1, maximum_row + 1)}
    replacements[0] = variable(0)
    shifted_variable = add(variable(0), {(): Fraction(1)})
    for degree in range(1, maximum_row + 1):
        expected_cumulant = Fraction(0 if degree == 1 else -factorial(degree - 1))
        assert substitute(recurrence(degree, 1), replacements) == ({(): expected_cumulant} if expected_cumulant else {})
        expected_appell = add(polynomial_power(shifted_variable, degree), scale(polynomial_power(shifted_variable, degree - 1), -degree))
        assert substitute(appell(degree), replacements) == expected_appell
    double_zero_polynomial = multiply(polynomial_power(shifted_variable, 2), add(variable(0), {(): Fraction(-2)}))
    assert substitute(appell(3), replacements) == double_zero_polynomial
    print(json.dumps({
        'status': 'pass',
        'arithmetic': 'exact rational sparse polynomial arithmetic',
        'all_column_identity': {'rows': [1, maximum_row], 'columns': [1, maximum_column], 'cases': quotient_cases},
        'first_column_logarithm_and_partition_formula': {'rows': [1, maximum_row]},
        'monomial_counts': row_counts,
        'integral_coefficients_and_row_sums': {'rows': [1, maximum_row]},
        'constant_variable_stirling_specialization': {'rows': [1, maximum_row]},
        'moment_and_appell_recurrences': {'degrees': [0, maximum_row - 1]},
        'oeis_A263634_revision_166_initial_coefficients': len(expected_oeis),
        'signed_A130850_eulerian_specialization': {'degrees': [0, maximum_row - 1]},
        'cycle_bell_lah_substitutions': {'rows': [1, family_order], 'families': 3},
        'exponential_polynomial_normalization_and_appell_example': {'rows': [1, maximum_row], 'double_zero_at': -1, 'third_appell_polynomial': 'z^3 - 3*z - 2 = (z+1)^2*(z-2)'},
        'scope': 'Finite polynomial identities; the general statements have the written proofs in note.pdf.'
    }, indent=2))


if __name__ == '__main__':
    main()
