class TypeCheckError(Exception):
    pass


class ArgumentTypeError(TypeCheckError):
    pass


class ReturnTypeError(TypeCheckError):
    pass


def typecheck_arguments(*args_types, **kwargs_types):
    """
    Require that the args and kwargs of the decorated function
    match the specified types.

    Throws ArgumentTypeError if there is a type mismatch.
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


def typecheck_return(return_type):
    """
    Require that the args and kwargs of the decorated function
    match the specified types.

    Throws ReturnTypeError if there is a type mismatch.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            retval = func(*args, **kwargs)

            # check return type
            if not isinstance(retval, return_type):
                msg = "Return type of '{}' where type '{}' was required.".format(type(retval), return_type)
                raise ReturnTypeError(msg)

            return retval
        return wrapper
    return decorator


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


print takes_int_outputs_string(1)
# print takes_int_outputs_string("bad")

print takes_int_and_kwarg_string_outputs_string(1, foo='bang')
