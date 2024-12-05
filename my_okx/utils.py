async def afh(func, asynchrony, *args, **kwargs):
    """Async Function Handler"""
    if asynchrony:
        result = await func(*args, **kwargs)
    else:
        result = func(*args, **kwargs)
    return result
