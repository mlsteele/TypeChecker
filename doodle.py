from typechecker import typecheck_arguments, typecheck_return, typecheck_exception


@typecheck_arguments(int)
def takes_int_outputs_string(n):
    if isinstance(n, int):
        return "a-ok!"
    else:
        return 404


@typecheck_arguments(int, foo=type(""))
@typecheck_return(str)
def takes_int_and_kwarg_string_outputs_string(n, foo=4):
    if isinstance(n, int) and isinstance(foo, type("")):
        return "a-ok!"
    else:
        return 404


@typecheck_exception(NameError, ValueError)
def can_throw_a_thing():
    raise ValueError("omg a value error")


print takes_int_outputs_string(1)
# print takes_int_outputs_string("bad")

print takes_int_and_kwarg_string_outputs_string(1, foo='bang')

print can_throw_a_thing()
