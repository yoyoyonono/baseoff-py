import math
import functools

shortNames: dict[int, str] = {}


def shortName(b: int) -> str:
    if b < 0:
        return f'-{shortName(b * -1)}'
    if b == 0:
        return ''
    minLen = 3
    if len(shortNames) >= b:
        if len(shortNames) not in shortNames:
            raise ArithmeticError
        return shortNames[b]
    for i in range(len(shortNames) + 1, b + 1):
        bn = ''.join(filter(lambda x: x not in "' ", baseName(i).upper()))
        abbv = bn[0:minLen]
        if len(bn) > minLen:
            bn = abbv + ''.join(filter(lambda x: x not in "AEIOU", bn[3:]))
        k = 1
        abbvLen = minLen
        while abbv in shortNames.values():
            nextOption = getAbbv(bn, k)
            if len(nextOption) == abbvLen:
                abbv = nextOption
            elif nextOption == " ":
                k = 0
                abbvLen += 1
                if abbvLen > len(bn):
                    return ""
            k += 1
            while bin(k).count('1') != abbvLen:
                k += 1
        shortNames[i] = abbv
    return shortNames[b]


def getAbbv(s: str, k: int) -> str:
    str1: str = s[0]
    bits = bin(k)[2:]
    if len(bits) >= len(s):
        return ' '
    for i in range(1, len(s)):
        if len(bits) >= i + 1 and bits[-1 * (i + 1)] == '1':
            str1 += s[i]
    return str1


def baseName(b: int) -> str:
    return removeHyphens(hyphenatedBaseName(b))


def neutralNumber(b: int) -> str:
    return removeHyphens(hyphenatedNumberName(b))


def removeHyphens(name: str) -> str:
    return name.replace('i-i', '-i').replace('i-u', 'i-').replace('e-u', '-u').replace('e-e', '-e').replace('o-i', '-i').replace('o-u', '-u').replace('o-e', '-e').replace('o-o', '-o').replace('a-i', '-i').replace('a-u', '-u').replace('a-e', '-e').replace('a-o', '-o').replace('-', '')


@functools.cache
def hyphenatedBaseName(b: int) -> str:
    name = ''
    if b < 0:
        return f'nega-{hyphenatedBaseName(b * -1)}'

    match b:
        case 0:
            return 'nullary'
        case 1:
            return 'unary'
        case 10:
            return 'decimal'
        case 13:
            return 'baker\'s dozenal'
        case _:
            return suffix(b)


@functools.cache
def hyphenatedNumberName(b: int) -> str:
    name = ''
    if b < 0:
        return f'nega-{hyphenatedNumberName(b * -1)}'

    match b:
        case 0:
            return 'null'
        case 1:
            return 'una'
        case 10:
            return 'dec'
        case 13:
            return 'baker\'s dozen'
        case _:
            return suffix_alt(b)


@functools.cache
def suffix(n: int) -> str:
    match n:
        case 2:
            return 'binary'
        case 3:
            return 'trinary'
        case 4:
            return 'quaternary'
        case 5:
            return 'quinary'
        case 6:
            return 'seximal'
        case 7:
            return 'septimal'
        case 8:
            return 'octal'
        case 9:
            return 'nonary'
        case 10:
            return 'gesimal'
        case 11:
            return 'elevenary'
        case 12:
            return 'dozenal'
        case 13:
            return 'ker\'s dozenal'
        case 16:
            return 'hex'
        case 17:
            return 'suboptimal'
        case 20:
            return 'vigesimal'
        case 36:
            return 'niftimal'
        case 100:
            return 'centesimal'
        case _:
            factor = factorize(n)
            if factor == 1:
                return f'un-{suffix(n - 1)}'
            else:
                return f'{prefix(n // factor)}-{suffix(factor)}'


@functools.cache
def suffix_alt(n: int) -> str:
    match n:
        case 2:
            return 'bin'
        case 3:
            return 'tri'
        case 4:
            return 'quater'
        case 5:
            return 'quin'
        case 6:
            return 'sex'
        case 7:
            return 'sept'
        case 8:
            return 'oct'
        case 9:
            return 'non'
        case 10:
            return 'ges'
        case 11:
            return 'eleven'
        case 12:
            return 'dozen'
        case 13:
            return 'ker\'s dozen'
        case 16:
            return 'hex'
        case 17:
            return 'subopt'
        case 20:
            return 'viges'
        case 36:
            return 'nift'
        case 100:
            return 'cent'
        case _:
            factor = factorize(n)
            if factor == 1:
                return f'un-{suffix_alt(n - 1)}'
            else:
                return f'{prefix(n // factor)}-{suffix_alt(factor)}'


@functools.cache
def prefix(n: int) -> str:
    match n:
        case 2:
            return 'bi'
        case 3:
            return 'tri'
        case 4:
            return 'tetra'
        case 5:
            return 'penta'
        case 6:
            return 'hexa'
        case 7:
            return 'hepta'
        case 8:
            return 'octo'
        case 9:
            return 'enna'
        case 10:
            return 'deca'
        case 11:
            return 'leva'
        case 12:
            return 'doza'
        case 13:
            return 'baker'
        case 16:
            return 'tesser'
        case 17:
            return 'mal'
        case 20:
            return 'icosi'
        case 36:
            return 'feta'
        case 100:
            return 'hecto'
        case _:
            factor = factorize(n)
            if factor == 1:
                return f'hen-{prefix(n - 1)}s-na'
            else:
                return f'{prefix(n // factor)}-{prefix(factor)}'


@functools.cache
def factorize(n: int) -> int:
    n = int(n)
    bestFactor = 1
    shortestName = float('inf')
    for i in range(math.ceil(math.sqrt(n)), n):
        if n % i == 0:
            roots = rootsInName(i) + rootsInName(n / i)
            if roots < shortestName:
                shortestName = roots
                bestFactor = i
    return bestFactor


@functools.cache
def rootsInName(b: int) -> int:
    nr = hyphenatedBaseName(b)
    n = nr.replace('-', '')
    return len(nr) - len(n) + 1


if __name__ == '__main__':
    import rich.progress
    import rich.console
    import rich.table
    import baseconv
    base6 = baseconv.BaseConverter("012345")
    base12 = baseconv.BaseConverter("0123456789EX")
    base36 = baseconv.BaseConverter("0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ")
    bases = rich.table.Table(title="Base Names")
    bases.add_column("dec")
    bases.add_column("sex")
    bases.add_column("doz")
    bases.add_column("hex")
    bases.add_column("nif")
    bases.add_column("occ")
    bases.add_column("name")
    bases.add_column("base")
    bases.add_column("abbv")
    for i in rich.progress.track(range(int(input("lower bound (default 1): ") or 1), int(input("upper bound (default 100): ") or 100) + 1)):
        bases.add_row(str(i), base6.encode(i), base12.encode(i), baseconv.base16.encode(
            i), base36.encode(i), baseconv.base64.encode(i), neutralNumber(i), baseName(i), shortName(i))
    console = rich.console.Console()
    console2 = rich.console.Console(file=open('bases.txt', 'w'))
    console.print(bases)
    console2.print(bases)
