import os, re
import functools

def read_template_file(path):
    cfg = dict()
    with open(path, 'r') as fd:
        for line in fd:
            # ignore define { }
            if re.search(r'^\s*define.*', line) or re.search(r'^\s*\}$', line): continue
            # ignore empty lines
            if re.search(r'^$', line): continue
            # ignore lines that start with # or ;
            if re.search(r'^[;#]', line): continue

            line = re.sub(r'[;#].*$', '', line)

            k, v = re.split(r'\s+', line.strip(), 1)

            if cfg.get(k, None):
                if isinstance(cfg[k], list):
                    cfg[k].append(v)
                else:
                    save = cfg[k]
                    cfg[k] = [save, v]
            else:
                cfg[k] = v

    return cfg

def find(path, name):
    results = []
    for cur_dir, subdirs, files in os.walk(path):
        for f in files:
            if f == name:
                results.append(os.path.join(cur_dir, f))

    return results


def underscoreize(name):
    out = []
    for c in name:
        if ord(c) < 96: out.append(c.lower())
        else: out[-1] += c

    return "_".join(out)

def pluralize(name):
    if name[-1:] == 'y':
        return "%sies" % name[:-1]
    else:
        return "%ss" % name


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
