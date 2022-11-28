I = 'int'
F = 'float'
B = 'bool'
S = 'string'

class Cubo:
    def __init__(self):
        # Lista con las combinaciones necesarias para devolver el tipo de dato del resultado
        self.semanticCube = {
            (I, I, '*'): I,
            (I, I, '/'): F,
            (I, I, '+'): I,
            (I, I, '-'): I,
            (I, I, '>'): B,
            (I, I, '<'): B,
            (I, I, '=='): B,
            (I, I, '!='): B,
            (I, I, '&&'): B,
            (I, I, '||'): B,
            (I, F, '*'): F,
            (I, F, '/'): F,
            (I, F, '+'): F,
            (I, F, '-'): F,
            (I, F, '>'): B,
            (I, F, '<'): B,
            (I, F, '=='): B,
            (I, F, '!='): B,
            (I, F, '&&'): B,
            (I, F, '||'): B,
            (I, B, '&&'): B,
            (I, B, '||'): B,
            (F, I, '*'): F,
            (F, I, '/'): F,
            (F, I, '+'): F,
            (F, I, '-'): F,
            (F, I, '>'): B,
            (F, I, '<'): B,
            (F, I, '=='): B,
            (F, I, '!='): B,
            (F, I, '&&'): B,
            (F, I, '||'): B,
            (F, F, '*'): F,
            (F, F, '/'): F,
            (F, F, '+'): F,
            (F, F, '-'): F,
            (F, F, '>'): B,
            (F, F, '<'): B,
            (F, F, '=='): B,
            (F, F, '!='): B,
            (F, F, '&&'): B,
            (F, F, '||'): B,
            (F, B, '&&'): B,
            (F, B, '||'): B,
            (B, I, '&&'): B,
            (B, I, '||'): B,
            (B, F, '&&'): B,
            (B, F, '||'): B,
            (B, B, '=='): B,
            (B, B, '!='): B,
            (B, B, '&&'): B,
            (B, B, '||'): B,
            (I, I, '='): I,
            (F, F, '='): F,
            (S, S, '='): S,
            (B, B, '='): B
        }

    def type_match(self, left_operand, right_operand, op):
        if (left_operand, right_operand, op) in self.semanticCube:
            return self.semanticCube[(left_operand, right_operand, op)]
        return None