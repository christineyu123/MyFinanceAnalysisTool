def skip_exception_decorator(func):
    def utility_func(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print("not found")
            return None

    return utility_func
