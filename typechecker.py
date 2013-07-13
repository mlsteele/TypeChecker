"""
TypeChecker

Python type checking.
Provides decorators for type checking
- arguments
- return values
- exceptions

Useful as a debugging and inline testing tool.
"""


class TypeCheckError(Exception):
    """ Base exception for typechecker """
    pass


class ArgumentTypeError(TypeCheckError):
    """ Exception for incorrect argument type. """


class ReturnTypeError(TypeCheckError):
    """ Exception for incorrect return type. """


class ExceptionTypeError(TypeCheckError):
    """ Exception for incorrect exception type. """


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
                msg = "Return of type '{}' where type '{}' was required.".format(type(retval), return_type)
                raise ReturnTypeError(msg)

            return retval
        return wrapper
    return decorator


def typecheck_exception(*exception_types):
    """
    Require that IF the decorated function raises and Exception
        THEN it be derived from on of those in `*exception_types`

    Throws the original exception if all goes well,
    Throws ExceptionTypeError if a non-matching exception
        is thrown by the decorated function.
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                ok = any([isinstance(exc, exc_type)
                          for exc_type in exception_types])
                if ok:
                    raise exc
                else:
                    msg = "Exception of type '{}' is not one of the allowed exception types.".format(type(exc))
                    raise ExceptionTypeError(msg)
        return wrapper
    return decorator
