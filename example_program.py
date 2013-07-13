from typechecker import typecheck_arguments, typecheck_return, typecheck_exception


@typecheck_arguments(int, float, c=tuple)
@typecheck_exception(NameError, ValueError)
@typecheck_return(type)
def finicky_funcion(a, b, c='doodles'):
    class Foo(object):
        pass
    return Foo


finicky_funcion(1, 2.0, c=(4,))
