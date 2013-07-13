class TypeCheckError(Exception):
    pass


class ArgumentTypeError(TypeCheckError):
    pass


def typecheck_args(*args_types, **kwargs_types):
    def decorator(func):
        def wrapper(*args, **kwargs):
            # check arguments
            for (arg, required_type) in zip(args, args_types):
                if not isinstance(arg, required_type):
                    msg = "Argument of type {} where type {} was required.".format(type(arg), required_type)
                    raise ArgumentTypeError(msg)

            # check kwarguments
            for key in kwargs_types:
                if not isinstance(kwargs[key], kwargs_types[key]):
                    msg = "Kwargument of type {} where type {} was required.".format(type(arg), required_type)
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


print takes_int_outputs_string(1)
print takes_int_outputs_string("bad")
