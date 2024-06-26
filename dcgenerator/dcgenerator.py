import logging
from aqt import gui_hooks
from aqt.utils import showInfo
import os

addon_path = os.path.dirname(__file__)
generators_path = os.path.join(addon_path, "content_generators")
prefix = "dcg#"

logging.basicConfig(level=logging.INFO)


def run_script(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            script_contents = f.read()
            exec(script_contents)
    except Exception as e:
        logging.error(f"Error executing script {path}: {e}")
        raise


def dynamic_content(card):
    try:
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
                    run_script(generator_file_path)
                else:
                    showInfo(f"Generation script {generator_file_path} does not exist for tag: {tag}")

            # Should only contain one dynamic tag
            break
    except Exception as e:
        logging.error(f"Error processing dynamic content for card {card.id}: {e}")


def main():
    gui_hooks.reviewer_did_show_question.append(dynamic_content)

