from aqt.utils import showInfo
import os
from anki import hooks
from anki.template import TemplateRenderContext

addon_path = os.path.dirname(__file__)
generators_path = os.path.join(addon_path, "content_generators")
filter_name = "dcg"


def get_script_dict(path, exec_dict):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            script_contents = f.read()
            exec(script_contents, exec_dict)

    except Exception as e:
        showInfo(f"Error executing script: {e}")
        raise


def my_field_filter(field_text: str, field_name: str, filter_name: str, context: TemplateRenderContext) -> str:
    if not filter_name.startswith(filter_name):
        # not our filter, return string unchanged
        return field_text

    # split the name into the 'info' prefix, and the rest
    try:
        (label, card_property, script_name) = filter_name.split("-", maxsplit=2)
    except ValueError:
        return invalid_name(filter_name)

    # Get Generator file path
    generator_file_path = os.path.join(generators_path, f"{script_name}.py")

    # Generate front and back
    exec_dict = {}
    get_script_dict(generator_file_path, exec_dict)

    if 'generate_front' not in exec_dict:
        showInfo("Required method 'generate_front()' not found")
        return

    if 'generate_back' not in exec_dict:
        showInfo("Required method 'generate_back()' not found")
        return

    front_text = exec_dict['generate_front']()
    back_text = exec_dict['generate_back']()

    # call the appropriate function
    if card_property == "front":
        return front_text
    elif card_property == "back":
        return back_text
    else:
        return invalid_name(filter_name)


def invalid_name(filter_name: str) -> str:
    return f"invalid filter name: {filter_name}"


def main():
    hooks.field_filter.append(my_field_filter)
