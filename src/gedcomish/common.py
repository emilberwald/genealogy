import datetime
import inspect
import os
import pathlib
import re
import uuid
import warnings
import itertools
from enum import Enum
from typing import Callable, Iterable, List, Optional, Tuple, Union


class Meta(type):
    @classmethod
    def __prepare__(metaclass, name, bases, **kwds):
        """
            __prepare__
            :param metaclass:   classdef keyword argument 'metaclass'
            :param name:        classdef name
            :param bases:       classdef positional arguments
            :param **kwds:      classdef keyword arguments (sans 'metaclass')
                                NOTE: same as in classdef, passed by value
            :return:            namespace
        """
        return super().__prepare__(metaclass, name, bases, **kwds)

    @staticmethod
    def __new__(metaclass, name, bases, namespace, **kwds):
        """
            __new__
            :param metaclass:   classdef keyword argument 'metaclass'
            :param name:        classdef name
            :param bases:       classdef positional arguments
            :param namespace:   namespace
                                NOTE:
                                if '__classcell__' is present, it must be included in the call to super().
            :param **kwds:      classdef keyword arguments (sans 'metaclass')
                                NOTE: same as in classdef, passed by value
            :return:            <class 'name'>
        """
        return super().__new__(metaclass, name, bases, namespace)

    def __init__(classname, name, bases, namespace, **kwds):
        """
            __init__
            :param classname:       <class 'name'>
            :param name:            classdef name
            :param bases:           classdef positional arguments
            :param namespace:       namespace
            :param **kwds:          classdef keyword arguments (sans 'metaclass')
                                    NOTE: same as in classdef, passed by value
            :return:                None
            NOTE:
            must call: super().__init__([args...]).
        """
        for key, value in kwds.items():
            if not hasattr(classname, key):
                setattr(classname, key, value)
            else:
                warnings.warn(f"Could not enter {key}:{value} into class dictionary", Warning)
        super().__init__(name, bases, namespace, **kwds)

    def __call__(classname, *args, **kwargs):
        """
            __call__
            :param classname:   <class 'name'>
            :param *args:       class call positional arguments (instantiation of <class 'name'>)
            :param **kwargs:    class call keyword arguments (instantiation of <class 'name'>)
            :return:            <name object at 0x...>
            NOTE:
            <class 'name'>(*ARGS, **KWARGS)
                __call__(<class 'name'>, *args, **kwargs)
                    <class 'name'>:         __init__(<name object at 0x...>, *args, **kwargs) -> None
                    <class 'name'> bases:   __init__(<name object at 0x...>, [args...]) -> None
            -> <name object at 0x...>
        """
        return super().__call__(*args, **kwargs)


class Common(metaclass=Meta):
    pass


class XREF_ID(Common):
    def __init__(self, identifier=None):
        if isinstance(identifier, uuid.UUID):
            self.id = str(identifier).replace("-", "")[0:20]
        elif identifier is not None:
            self.id = str(identifier)[0:20]
        else:
            self.id = str(uuid.uuid1()).replace("-", "")[0:20]

    def __str__(self):
        return f"@{self.id}@"


class GEDCOM_SYNTAX:
    digit = f"[\u0030-\u0039]"
    alpha = f"[\u0041-\u005A|\u0061-\u007A]"
    alphanum = f"[{alpha}|{digit}]"
    non_zero_digit = f"[\u0031-\u0039]"
    level = f"[{digit}|{non_zero_digit}{digit}]"
    tag = f"[\u005F|{alphanum}]+"
    identifier_string = f"{alphanum}+"
    at = "\u0040"
    xref_ID = f"{at}{identifier_string}{at}"
    pointer = f"{xref_ID}"
    escape_text = f"[{alphanum}|\u0020]+"
    escape = f"\u0040\u0023{escape_text}\u0040"
    delim = f"\u0020"
    line_char = f"[^\u0000-\u0008\u000A-\u001F\u00FF]"
    line_text = f"{line_char}+"
    line_item = f"[{escape}|{line_text}|{escape}{delim}{line_text}]"
    line_value = f"[{pointer}|{line_item}]"
    carriage_return = "\u000D"
    line_feed = "\u000A"
    terminator = f"[{carriage_return}|{line_feed}|{carriage_return}{line_feed}]"
    null = f""


class GEDCOM_LINE:
    def __init__(
        self, *, level: int, tag: str, xref_id: XREF_ID = None, line_value: str = None,
    ):
        self.level = level
        self.xref_id = xref_id
        self.tag = tag
        self.line_value = line_value

    def __str__(self):
        return (
            " ".join([str(val) for val in [self.level, self.xref_id, self.tag, self.line_value] if val is not None])
            + "\n"
        )


class Primitive(Common):
    def __init__(self, *args, **kwargs):
        self.value = str()
        for arg in args:
            self.value += str(arg)
        for kwarg in kwargs:
            self.value += str(kwarg)

    def __str__(self):
        return self.value


class GEDCOM_LINES:
    def __init__(self):
        self.lines: List[Union[Callable[[int], GEDCOM_LINE], "GEDCOM_LINES"]] = list()

    def add_text(self, *, level_delta: int, tag: str, primitive: Primitive, xref_id: XREF_ID = None):
        try:

            def unicode_chunksplit(slicable, safe_chunksize: int):
                from_char = 0
                while from_char < len(slicable):
                    for to_char in range(from_char + safe_chunksize, from_char, -1):
                        if len(slicable[from_char:to_char].encode("utf-8")) <= safe_chunksize:
                            yield slicable[from_char:to_char]
                            from_char = to_char
                            break

            safe_chunksize = 255
            safe_chunksize -= len("99")
            if xref_id:
                safe_chunksize -= len(" ") + len(str(xref_id).encode("UTF-8"))
            if tag:
                safe_chunksize -= len(" ") + len(tag.encode("UTF-8"))
            safe_chunksize -= len(os.linesep)
            safe_chunksize -= len(" ")
            value = str(primitive)
            if isinstance(primitive, XREF_ID):
                pass
            else:
                value.replace("@", "@@")
            lines = value.split(os.linesep)
            if isinstance(primitive, Enum):
                primitive = primitive.value
            for line_no, line in enumerate(lines):
                for text_chunk_no, unicode_text_chunk in enumerate(unicode_chunksplit(line, safe_chunksize)):
                    if text_chunk_no == 0:
                        if line_no == 0:

                            def apply_text(
                                n, level_delta=level_delta, tag=tag, xref_id=xref_id, line_value=unicode_text_chunk
                            ):
                                return GEDCOM_LINE(
                                    level=n + level_delta, tag=tag, xref_id=xref_id, line_value=line_value
                                )

                            self.lines.append(apply_text)
                            continue
                        else:

                            def apply_cont(n, level_delta=level_delta, xref_id=xref_id, line_value=unicode_text_chunk):
                                return GEDCOM_LINE(
                                    level=n + level_delta + 1, tag="CONT", xref_id=xref_id, line_value=line_value
                                )

                            self.lines.append(apply_cont)
                    else:

                        def apply_conc(n, level_delta=level_delta, xref_id=xref_id, line_value=unicode_text_chunk):
                            return GEDCOM_LINE(
                                level=n + level_delta + 1, tag="CONC", xref_id=xref_id, line_value=line_value
                            )

                        if hasattr(primitive, "meta"):
                            if max(getattr(getattr(primitive, "meta"), "Size")) <= 248:
                                raise ValueError(
                                    f"'never uses CONC records for line values with a maximum length of 248 or less': "
                                    "{line}"
                                )
                            else:
                                self.lines.append(apply_conc)
        except Exception as ex:
            raise ex

    def add_primitives(self, level_delta: int, tag: str, *primitives: Optional[Primitive], xref_id: XREF_ID = None):
        if primitives:
            for primitive in primitives:
                if primitive:
                    print(f"\t\t<{level_delta} {tag} {primitive} {xref_id}>")
                    self.add_text(level_delta=level_delta, tag=tag, primitive=primitive, xref_id=xref_id)
        else:

            def apply(n, level_delta=level_delta, tag=tag, xref_id=xref_id):
                return GEDCOM_LINE(level=n + level_delta, tag=tag, xref_id=xref_id, line_value=None)

            print(f"\t\t<{level_delta} {tag} {primitives} {xref_id}>")
            self.lines.append(apply)

    def add_substructures(self, level_delta: int, *substructs: Optional["Substructure"]):
        if substructs:
            for substruct in substructs:
                if substruct:

                    def apply(n, level_delta=level_delta, substruct=substruct):
                        return substruct(n + level_delta)

                    print(f"\t\t<<{level_delta} {substructs}>>")
                    self.lines.append(apply)

    def __call__(self, level=int):
        return "".join([str(line(level)) for line in self.lines])


class Tag(Common):
    pass


class Pointer(Common):
    pass


class Option(Common):
    pass


class Substructure(Common):
    @classmethod
    def nested_classes(cls, *queries):
        inners = []
        for attrname in dir(cls):
            attr = getattr(cls, attrname)
            if isinstance(attr, type) and any(issubclass(attr, innercls) for innercls in queries):
                inners.append(attr)
        return inners

    def instances_of_nested_classes(self, *queries):
        inners = []
        for attrname in dir(self):
            attr = getattr(self, attrname)
            if isinstance(attr, Iterable):
                for subattr in attr:
                    if any(isinstance(subattr, innercls) for innercls in queries):
                        inners.append(subattr)
            elif not isinstance(attr, type) and any(
                isinstance(attr, innercls) for innercls in queries if innercls is not Iterable
            ):
                inners.append(attr)
        return inners

    @staticmethod
    def find_stuff(nested, base, level=0):
        if isinstance(nested, Primitive):
            if isinstance(nested, base):
                yield nested
        else:
            yield from (getattr(nested, attr) for attr in dir(nested) if isinstance(getattr(nested, attr), base))

    def itersource(self):
        file = inspect.getsourcefile(self.__class__)
        source = pathlib.Path(file).read_text()
        starts = list(re.finditer(fr"^(?=class)", source, re.MULTILINE))
        ends = starts[1:]
        for end, start in itertools.zip_longest(
            (end.start() if end else None for end in ends), (start.start() if start else None for start in starts)
        ):
            for m in re.finditer(fr"(?=class\s+{self.__class__.__name__}\s*\()", source[start:end]):
                yield source[start:end][m.start() :]

    def getsource(self, nesteds):
        def score(source, nesteds):
            tot = 0
            for nested in nesteds:
                if isinstance(nested, Iterable):
                    for subnested in nested:
                        tot += subnested.__class__.__name__ in source
                else:
                    tot += nested.__class__.__name__ in source
            return tot

        alternatives = [inspect.getsource(self.__class__), *self.itersource()]
        best = max(alternatives, key=lambda alternative, nesteds=nesteds: score(alternative, nesteds))
        return best

    @staticmethod
    def _is_reference_included(nested):
        for base in nested.__class__.__bases__:
            yield fr"{base.__name__}s\s*="
            yield fr"=\s*{base.__class__.__name__}"
            yield fr"=\s*Iterable\[{base.__class__.__name__}s[.]{base.__class__.__name__}\]"
        yield fr"{nested.__class__.__name__}\s*="
        yield fr"{nested.__class__.__name__}s\s*="
        yield fr"=\s*{nested.__class__.__name__}"
        yield fr"=\s*{nested.__class__.__qualname__}"
        yield fr"=\s*Iterable\[{nested.__class__.__name__}\]"
        yield fr"=\s*Iterable\[{nested.__class__.__qualname__}\]"

    def handle_nested(self, *, lines: GEDCOM_LINES, nested: Union[Primitive, "Substructure"], delta_level: int):
        if hasattr(nested, "delta_level") and getattr(nested, "delta_level"):
            nested_level = delta_level + getattr(nested, "delta_level")
            print(
                f"![{nested_level}\t{nested.__class__.__qualname__} <= {delta_level:+d} {getattr(nested, 'delta_level'):+d}]"
            )
        else:
            nested_level = delta_level

        tag = nested.__class__.__name__
        bases = [base for base in nested.__class__.__bases__ if base not in (XREF_ID, Primitive, Substructure)]
        xrefs: List[XREF_ID] = list()
        tag_with_value = False
        primitives: List[Primitive] = list()
        substructures: List[Substructure] = list()
        for base in bases:
            if issubclass(base, Primitive) and isinstance(nested, base):
                tag_with_value = True
                print(f"<is-tag-with-value-for-{base}:{nested}>")
                continue
            if isinstance(nested, base):
                print(f"<skip-self-{base}:{nested}>")
                continue
            if isinstance(nested, Pointer) and issubclass(base, XREF_ID):
                found = list(Substructure.find_stuff(nested, base))
                print(f"<xrefs-for-{base}:{found}>")
                xrefs.extend(found)
            if issubclass(base, Primitive):
                found = list(Substructure.find_stuff(nested, base))
                print(f"<primitives-for-{base}:{found}>")
                primitives.extend(found)
            if issubclass(base, Substructure):
                found = list(Substructure.find_stuff(nested, base))
                print(f"<substructures-for-{base}:{found}>")
                substructures.extend(found)
        if tag_with_value and isinstance(nested, Primitive):
            if str(nested):
                print(f"<tag-with-value>")
                lines.add_primitives(nested_level, tag, nested)
            else:
                print(f"<tag-with-value-without-value>")
                lines.add_primitives(nested_level, tag)
        if xrefs:
            print(f"<xrefs>")
            for xref in (xref for xref in xrefs if xref is not None):
                lines.add_primitives(nested_level, tag, xref_id=xref if xref else None)
        if primitives:
            print(f"<primitives>")
            lines.add_primitives(nested_level, tag, *primitives, xref_id=xrefs[0] if xrefs else None)
        if substructures:
            print(f"<substructures>")
            lines.add_substructures(nested_level, *substructures)
        try:
            if isinstance(nested, Substructure):
                print(f"<nested:call@{delta_level}>")
                nested(lines=lines, delta_level=delta_level)
            else:
                print(f"<nested:skip>")
        except Exception as e:
            print(f"<nested:except:{e}>")

    def __call__(self, *, lines: GEDCOM_LINES, delta_level=0):
        print(f"\n[{delta_level}\t{self.__class__.__qualname__}]")
        if hasattr(self, "delta_level") and getattr(self, "delta_level"):
            delta_level = delta_level + getattr(self, "delta_level")
            print(f"![{delta_level}\t{self.__class__.__qualname__} => {getattr(self, 'delta_level'):+d}]")

        if isinstance(self, Tag):
            print(f"<Tag>")
            lines.add_primitives(delta_level, self.__class__.__name__)
        elif isinstance(self, Pointer):
            print(f"<Pointer>")
            lines.add_primitives(delta_level, self.__class__.__name__, xref_id=self)
        elif isinstance(self, XREF_ID):
            print(f"<XREF_ID>")
            lines.add_primitives(delta_level, self.__class__.__name__, self)

        nesteds = list(self.instances_of_nested_classes(XREF_ID, Primitive, Substructure))

        clssource = self.getsource(nesteds)

        nesteds = sorted(
            nesteds,
            key=lambda nested, clssource=clssource: result.start()
            if (
                result := re.search(
                    r"|".join(
                        (fr"class\s+{nested.__class__.__name__}", *Substructure._is_reference_included(nested=nested))
                    ),
                    clssource,
                )
            )
            else float("inf"),
        )
        print(f"<nesteds:{nesteds}>\n{'*'*80}\n{clssource}\n{'*'*80}\n")
        for nested in nesteds:

            print(f"<nested:{nested.__class__.__qualname__}:{nested}>")
            is_iteration_included = isinstance(nested, Iterable)
            is_reference_included = re.search(r"|".join(Substructure._is_reference_included(nested=nested)), clssource)

            if is_iteration_included:
                print("<is_iteration_included>")
                for subnested in nested:
                    print(f"<subnested:handle_nested@+1:{delta_level+1}>")
                    self.handle_nested(lines=lines, nested=subnested, delta_level=delta_level + 1)
            elif is_reference_included:
                if isinstance(nested, Substructure):
                    print(f"<is_reference_included:handle_nested@+1:{delta_level+1}>")
                    self.handle_nested(lines=lines, nested=nested, delta_level=delta_level + 1)
                else:
                    print(f"<is_reference_included:skip:{nested}>")
            else:
                print(f"<else:handle_nested@{delta_level}>")
                self.handle_nested(lines=lines, nested=nested, delta_level=delta_level)

        return lines


def get_month(date: datetime.datetime):
    return [None, "JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"][date.month]


def try_strptime(date_phrase: str):
    date_phrase = date_phrase.strip().rstrip(".xX-")
    for fmt in [r"%Y-%m-%d", r"%Y-%m", r"%Y"]:
        try:
            return datetime.datetime.strptime(date_phrase, fmt)
        except Exception as _:
            pass
    return None


def get_gedcom_date(date_phrase: str):
    interpreted_date = try_strptime(date_phrase)
    if interpreted_date:
        return " ".join(
            [
                "INT",
                str(interpreted_date.day),
                get_month(interpreted_date),
                str(interpreted_date.year),
                "".join(["(", date_phrase, ")"]),
            ]
        )
    else:
        return "".join(["(", date_phrase, ")"])
