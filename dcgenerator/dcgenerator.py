from aqt import gui_hooks
from aqt.utils import showInfo
import os

addon_path = os.path.dirname(__file__)
generators_path = os.path.join(addon_path, "content_generators")
prefix = "dcg#"


def run_script(path):
    with open(path) as f:
        code = compile(f.read(), path, 'exec')
        exec(code)


def dynamic_content(card):
    # Get tags associated with the current card
    tags = card.note().tags

    showInfo(f"Tags for next card: {', '.join(tags)}")

    for tag in tags:
        if tag.startswith(prefix):
            # Get tag without prefix
            generator_file_path = os.path.join(
                generators_path,
                f"{tag[len(prefix):]}.py"
            )

            # Check if script exists
            if os.path.exists(generator_file_path):
                showInfo(f"Executing script: {generator_file_path}")

                # Attempt to execute script
                with open(generator_file_path, 'r', encoding='utf-8') as f:
                    script_contents = f.read()
                    exec(script_contents)
            else:
                showInfo(f"Generation script {generator_file_path} does not exist for tag: {tag}")

        # Should only contain one dynamic tag
        break


def main():
    gui_hooks.reviewer_did_show_question.append(dynamic_content)

