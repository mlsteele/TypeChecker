class TypeCheckError(Exception):
    pass


class ArgumentTypeError(TypeCheckError):
    pass


def typecheck_args(*args_types, **kwargs_types):
    """
    Require that the args and kwargs of the decorated function
    match the specified types.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # check arguments
            for (arg, required_type) in zip(args, args_types):
                if not isinstance(arg, required_type):
                    msg = "Argument of type '{}' where type '{}' was required.".format(type(arg), required_type)
                    raise ArgumentTypeError(msg)

            # check kwarguments
            for key in kwargs_types:
                if not key in kwargs:
                    msg = "Missing kwarg '{}'".format(key)
                    raise ArgumentTypeError(msg)

                if not isinstance(kwargs[key], kwargs_types[key]):
                    msg = "Kwargument '{}' of type '{}' where type '{}' was required.".format(key, type(arg), required_type)
                    raise ArgumentTypeError(msg)

            # run original function
            return func(*args, **kwargs)
        return wrapper
    return decorator


@typecheck_args(int)
def takes_int_outputs_string(n):
    if isinstance(n, int):
        return "a-ok!"
    else:
        return 404


@typecheck_args(int, foo=type(""))
def takes_int_and_kwarg_string_outputs_string(n, foo=4):
    if isinstance(n, int) and isinstance(foo, type("")):
        return "a-ok!"
    else:
        return 404


print takes_int_outputs_string(1)
# print takes_int_outputs_string("bad")

print takes_int_and_kwarg_string_outputs_string(1, foo='bang')
