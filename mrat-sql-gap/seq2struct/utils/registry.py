import collections
import collections.abc
import inspect
import sys


_REGISTRY = collections.defaultdict(dict)


def register(kind, name):
    kind_registry = _REGISTRY[kind]

    def decorator(obj):
        if name in kind_registry:
            raise LookupError('{} already registered as kind {}'.format(name, kind))
        kind_registry[name] = obj
        return obj

    return decorator


def lookup(kind, name):
    if isinstance(name, collections.abc.Mapping):
        name = name['name']

    if kind not in _REGISTRY:
        raise KeyError('Nothing registered under "{}"'.format(kind))
    return _REGISTRY[kind][name]


def construct(kind, config, unused_keys=(), **kwargs):
    return instantiate(
            lookup(kind, config),
            config,
            unused_keys + ('name',),
            **kwargs)


def instantiate(callable, config, unused_keys=(), **kwargs):
    merged = {**config, **kwargs}
    signature = inspect.signature(callable.__init__)#https://github.com/awslabs/gap-text2sql/issues/3
    #print(f"[[[[[[[[[[[[[[[[[[[[[ {signature.parameters.items()} ]]]]]]]]]]]]]]]]]]]]]]]]]]]")
    for name, param in signature.parameters.items():
        if param.kind in (inspect.Parameter.POSITIONAL_ONLY, inspect.Parameter.VAR_POSITIONAL):
            raise ValueError('Unsupported kind for param {}: {}'.format(name, param.kind))

    if any(param.kind == inspect.Parameter.VAR_KEYWORD for param in signature.parameters.values()):
        return callable(**merged)

    missing = {}
    for key in list(merged.keys()):
        if key not in signature.parameters:
            if key not in unused_keys:
                missing[key] = merged[key]
            merged.pop(key)
    if missing:
        print('WARNING {}: superfluous {}'.format(callable, missing), file=sys.stderr)
    return callable(**merged)
