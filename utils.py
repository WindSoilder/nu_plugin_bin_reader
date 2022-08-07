def kaitai_obj_to_dict(obj):
    if hasattr(obj, "__dict__"):
        result = {}
        for k, v in obj.__dict__.items():
            if not k.startswith("_"):
                result[k] = kaitai_obj_to_dict(v)
        return result
    elif isinstance(obj, list):
        result = []
        for item in obj:
            result.append(kaitai_obj_to_dict(item))
        return result
    else:
        return obj


def to_nu_value(obj, span):
    return {"Value": to_nu_value_impl(obj, span)}


def to_nu_value_impl(obj, span):
    # check for single builtin type.
    nu_type_table = {
        str: "String",
        int: "Int",
        float: "Float",
    }
    obj_type = type(obj)
    if obj_type in nu_type_table:
        return {nu_type_table[obj_type]: {"val": obj, "span": span}}
    # dict should convert to Record.
    if isinstance(obj, dict):
        cols = []
        values = []
        for k, v in obj.items():
            cols.append(k)
            values.append(to_nu_value_impl(v, span))
        return {"Record": {"cols": cols, "vals": values, "span": span}}
    # list should convert to List.
    elif isinstance(obj, list):
        values = []
        for item in obj:
            values.append(to_nu_value_impl(item, span))
        return {"List": {"vals": values, "span": span}}
    # bytes should convert to nushell Bytes
    elif isinstance(obj, (bytes, bytearray)):
        return {
            "Binary": {
                "val": list(obj),
                "span": span,
            }
        }
    raise RuntimeError


def nu_error(err_type, msg, span):
    return {"Error": {"label": err_type, "msg": msg, "span": span}}
