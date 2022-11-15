I = 'int'
F = 'float'
C = 'char'
B = 'bool'
ERROR = 'err'


def get_cubo():
    cubo = {}
    cubo[I] = {}
    cubo[I][I] = {}
    cubo[I][F] = {}
    cubo[I][C] = {}
    cubo[I][B] = {}

    cubo[I][I]['+'] = I
    cubo[I][I]['-'] = I
    cubo[I][I]['*'] = I
    cubo[I][I]['/'] = I
    cubo[I][I]['&&'] = ERROR
    cubo[I][I]['||'] = ERROR
    cubo[I][I]['>'] = B
    cubo[I][I]['<'] = B
    cubo[I][I]['>='] = B
    cubo[I][I]['<='] = B
    cubo[I][I]['=='] = B

    cubo[I][F]['+'] = F
    cubo[I][F]['-'] = F
    cubo[I][F]['*'] = F
    cubo[I][F]['/'] = F
    cubo[I][F]['&&'] = ERROR
    cubo[I][F]['||'] = ERROR
    cubo[I][F]['>'] = B
    cubo[I][F]['<'] = B
    cubo[I][F]['>='] = B
    cubo[I][F]['<='] = B
    cubo[I][F]['=='] = B

    cubo[I][C]['+'] = ERROR
    cubo[I][C]['-'] = ERROR
    cubo[I][C]['*'] = ERROR
    cubo[I][C]['/'] = ERROR
    cubo[I][C]['&&'] = ERROR
    cubo[I][C]['||'] = ERROR
    cubo[I][C]['>'] = ERROR
    cubo[I][C]['<'] = ERROR
    cubo[I][C]['>='] = ERROR
    cubo[I][C]['<='] = ERROR
    cubo[I][C]['=='] = ERROR

    cubo[I][B]['+'] = ERROR
    cubo[I][B]['-'] = ERROR
    cubo[I][B]['*'] = ERROR
    cubo[I][B]['/'] = ERROR
    cubo[I][B]['&&'] = ERROR
    cubo[I][B]['||'] = ERROR
    cubo[I][B]['>'] = ERROR
    cubo[I][B]['<'] = ERROR
    cubo[I][B]['>='] = ERROR
    cubo[I][B]['<='] = ERROR
    cubo[I][B]['=='] = ERROR

    cubo[F] = {}
    cubo[F][I] = {}
    cubo[F][F] = {}
    cubo[F][C] = {}
    cubo[F][B] = {}

    cubo[F][I]['+'] = F
    cubo[F][I]['-'] = F
    cubo[F][I]['*'] = F
    cubo[F][I]['/'] = F
    cubo[F][I]['&&'] = ERROR
    cubo[F][I]['||'] = ERROR
    cubo[F][I]['>'] = B
    cubo[F][I]['<'] = B
    cubo[F][I]['>='] = B
    cubo[F][I]['<='] = B
    cubo[F][I]['=='] = B

    cubo[F][F]['+'] = F
    cubo[F][F]['-'] = F
    cubo[F][F]['*'] = F
    cubo[F][F]['/'] = F
    cubo[F][F]['&&'] = ERROR
    cubo[F][F]['||'] = ERROR
    cubo[F][F]['>'] = B
    cubo[F][F]['<'] = B
    cubo[F][F]['>='] = B
    cubo[F][F]['<='] = B
    cubo[F][F]['=='] = B

    cubo[F][C]['+'] = ERROR
    cubo[F][C]['-'] = ERROR
    cubo[F][C]['*'] = ERROR
    cubo[F][C]['/'] = ERROR
    cubo[F][C]['&&'] = ERROR
    cubo[F][C]['||'] = ERROR
    cubo[F][C]['>'] = ERROR
    cubo[F][C]['<'] = ERROR
    cubo[F][C]['>='] = ERROR
    cubo[F][C]['<='] = ERROR
    cubo[F][C]['=='] = ERROR

    cubo[F][B]['+'] = ERROR
    cubo[F][B]['-'] = ERROR
    cubo[F][B]['*'] = ERROR
    cubo[F][B]['/'] = ERROR
    cubo[F][B]['&&'] = ERROR
    cubo[F][B]['||'] = ERROR
    cubo[F][B]['>'] = ERROR
    cubo[F][B]['<'] = ERROR
    cubo[F][B]['>='] = ERROR
    cubo[F][B]['<='] = ERROR
    cubo[F][B]['=='] = ERROR

    cubo[C] = {}
    cubo[C][I] = {}
    cubo[C][F] = {}
    cubo[C][C] = {}
    cubo[C][B] = {}

    cubo[C][I]['+'] = ERROR
    cubo[C][I]['-'] = ERROR
    cubo[C][I]['*'] = ERROR
    cubo[C][I]['/'] = ERROR
    cubo[C][I]['&&'] = ERROR
    cubo[C][I]['||'] = ERROR
    cubo[C][I]['>'] = ERROR
    cubo[C][I]['<'] = ERROR
    cubo[C][I]['>='] = ERROR
    cubo[C][I]['<='] = ERROR
    cubo[C][I]['=='] = ERROR

    cubo[C][F]['+'] = ERROR
    cubo[C][F]['-'] = ERROR
    cubo[C][F]['*'] = ERROR
    cubo[C][F]['/'] = ERROR
    cubo[C][F]['&&'] = ERROR
    cubo[C][F]['||'] = ERROR
    cubo[C][F]['>'] = ERROR
    cubo[C][F]['<'] = ERROR
    cubo[C][F]['>='] = ERROR
    cubo[C][F]['<='] = ERROR
    cubo[C][F]['=='] = ERROR

    cubo[C][C]['+'] = ERROR
    cubo[C][C]['-'] = ERROR
    cubo[C][C]['*'] = ERROR
    cubo[C][C]['/'] = ERROR
    cubo[C][C]['&&'] = ERROR
    cubo[C][C]['||'] = ERROR
    cubo[C][C]['>'] = ERROR
    cubo[C][C]['<'] = ERROR
    cubo[C][C]['>='] = ERROR
    cubo[C][C]['<='] = ERROR
    cubo[C][C]['=='] = B

    cubo[C][B]['+'] = ERROR
    cubo[C][B]['-'] = ERROR
    cubo[C][B]['*'] = ERROR
    cubo[C][B]['/'] = ERROR
    cubo[C][B]['&&'] = ERROR
    cubo[C][B]['||'] = ERROR
    cubo[C][B]['>'] = ERROR
    cubo[C][B]['<'] = ERROR
    cubo[C][B]['>='] = ERROR
    cubo[C][B]['<='] = ERROR
    cubo[C][B]['=='] = ERROR

    cubo[B] = {}
    cubo[B][I] = {}
    cubo[B][F] = {}
    cubo[B][C] = {}
    cubo[B][B] = {}

    cubo[B][I]['+'] = ERROR
    cubo[B][I]['-'] = ERROR
    cubo[B][I]['*'] = ERROR
    cubo[B][I]['/'] = ERROR
    cubo[B][I]['&&'] = ERROR
    cubo[B][I]['||'] = ERROR
    cubo[B][I]['>'] = ERROR
    cubo[B][I]['<'] = ERROR
    cubo[B][I]['>='] = ERROR
    cubo[B][I]['<='] = ERROR
    cubo[B][I]['=='] = ERROR

    cubo[B][F]['+'] = ERROR
    cubo[B][F]['-'] = ERROR
    cubo[B][F]['*'] = ERROR
    cubo[B][F]['/'] = ERROR
    cubo[B][F]['&&'] = ERROR
    cubo[B][F]['||'] = ERROR
    cubo[B][F]['>'] = ERROR
    cubo[B][F]['<'] = ERROR
    cubo[B][F]['>='] = ERROR
    cubo[B][F]['<='] = ERROR
    cubo[B][F]['=='] = ERROR

    cubo[B][C]['+'] = ERROR
    cubo[B][C]['-'] = ERROR
    cubo[B][C]['*'] = ERROR
    cubo[B][C]['/'] = ERROR
    cubo[B][C]['&&'] = ERROR
    cubo[B][C]['||'] = ERROR
    cubo[B][C]['>'] = ERROR
    cubo[B][C]['<'] = ERROR
    cubo[B][C]['>='] = ERROR
    cubo[B][C]['<='] = ERROR
    cubo[B][C]['=='] = ERROR

    cubo[B][B]['+'] = ERROR
    cubo[B][B]['-'] = ERROR
    cubo[B][B]['*'] = ERROR
    cubo[B][B]['/'] = ERROR
    cubo[B][B]['&&'] = B
    cubo[B][B]['||'] = B
    cubo[B][B]['>'] = ERROR
    cubo[B][B]['<'] = ERROR
    cubo[B][B]['>='] = ERROR
    cubo[B][B]['<='] = ERROR
    cubo[B][B]['=='] = B