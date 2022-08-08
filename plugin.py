# Example of using a Python script as a Nushell plugin
#
# The example uses JSON encoding but it should be a similar process using
# Cap'n Proto to move data between Nushell and the plugin. The only difference
# would be that you need to compile the schema file in order have the objects
# that decode and encode information that is read and written to stdin and stdout
#
# To register the plugin use:
# 	register <path-to-py-file> -e json
#
# Be carefull with the spans. Miette will crash if a span is outside the
# size of the contents vector. For this example we are using 0 and 1, which will
# point to the beginning of the contents vector. We strongly suggest using the span
# found in the plugin call head
#
# The plugin will be run using the active Python implementation. If you are in
# a Python environment, that is the Python version that is used
#
# Note: To keep the plugin simple and without dependencies, the dictionaries that
#   represent the data transferred between Nushell and the plugin are kept as
#   native Python dictionaries. The encoding and decoding process could be improved
#   by using libraries like pydantic and marshmallow
#
# This plugin uses python3
# Note: To debug plugins write to stderr using sys.stderr.write
import sys
import json

from kaitaistruct import BytesIO, KaitaiStream
from utils import to_nu_value, nu_error, kaitai_obj_to_dict


def signatures():
    """
    Multiple signatures can be sent to Nushell. Each signature will be registered
    as a different plugin function in Nushell.

    In your plugin logic you can use the name of the signature to indicate what
    operation should be done with the plugin
    """
    return {
        "Signature": [
            {
                "name": "from-binary",
                "usage": "Read binary data",
                "extra_usage": "",
                "input_type": "Any",
                "output_type": "Any",
                "required_positional": [
                    {
                        "name": "format",
                        "desc": "input binary format",
                        "shape": "String",
                        "var_id": None,
                    },
                ],
                "optional_positional": [],
                # FIXME: the rest positional is required, and it's not empty, I don't know if it's ok.
                "rest_positional": {
                    "name": "rest",
                    "desc": "rest value string",
                    "shape": "String",
                    "var_id": None,
                },
                "named": [
                    {
                        "long": "help",
                        "short": "h",
                        "arg": None,
                        "required": False,
                        "desc": "Display this help message",
                        "var_id": None,
                    },
                ],
                "search_terms": ["png"],
                "is_filter": False,
                "creates_scope": False,
                "category": "Experimental",
            }
        ]
    }


def process_call(plugin_call):
    """
    plugin_call is a dictionary with the information from the call
    It should contain:
            - The name of the call
            - The call data which includes the positional and named values
            - The input from the pipeline

    Use this information to implement your plugin logic
    """
    # Pretty printing the call to stderr
    # sys.stderr.write(json.dumps(plugin_call, indent=4))
    # sys.stderr.write("\n")

    # check input, make sure that the input is binary.
    call_info = plugin_call["CallInfo"]
    head_span = call_info["call"]["head"]
    if "input" not in call_info:
        return nu_error(
            "UnsupportedInput",
            "Input's type is nothing. This command only works with binary.",
            head_span,
        )
    pipeline_input = call_info["input"]
    if "Value" not in pipeline_input:
        return nu_error(
            "UnsupportedInput",
            "Input's type is nushell's Value. This command only works with binary.",
            head_span,
        )
    value = pipeline_input["Value"]
    if "Binary" not in value:
        # pick up value type, we can make sure that the input value contains only one key.
        value_type = list(value.keys())[0]
        return nu_error(
            "UnsupportedInput",
            f"Input's type is {value_type}. This command only works with binary.",
            value.get("span", head_span),
        )

    binary_data = bytearray(value["Binary"]["val"])
    format = call_info["call"]["positional"][0]["String"]["val"]
    try:
        return handle(binary_data, format, head_span)
    except Exception as e:
        return nu_error("Binary data parsing error", str(e), head_span)


def handle(binary_data, format, span):
    import importlib

    try:
        module = importlib.import_module(f"reader.{format}")
    except ModuleNotFoundError as e:
        raise RuntimeError(
            f"Can't find `{format}` binary reading lib, you should download it first"
        ) from e
    else:
        reader_class_name = "".join(format.replace("_", " ").title().split(" "))
        reader = getattr(module, reader_class_name)
        data = reader(KaitaiStream(BytesIO(binary_data)))
        py_dict = kaitai_obj_to_dict(data)
        return to_nu_value(py_dict, span)


def plugin():
    call_str = ",".join(sys.stdin.readlines())
    plugin_call = json.loads(call_str)

    if plugin_call == "Signature":
        signature = json.dumps(signatures())
        sys.stdout.write(signature)

    elif "CallInfo" in plugin_call:
        response = process_call(plugin_call)
        sys.stdout.write(json.dumps(response))

    else:
        # Use this error format if you want to return an error back to Nushell
        error = {
            "Error": {
                "label": "ERROR from plugin",
                "msg": "error message pointing to call head span",
                "span": {"start": 0, "end": 1},
            }
        }
        sys.stdout.write(json.dumps(error))


if __name__ == "__main__":
    plugin()
