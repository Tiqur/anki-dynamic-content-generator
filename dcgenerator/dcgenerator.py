from aqt.utils import showInfo
from anki.hooks import wrap
from aqt import gui_hooks
import os
from aqt.reviewer import Reviewer
from aqt.browser.card_info import CardInfoManager

front = "initial front"
back = "initial back"
addon_path = os.path.dirname(__file__)
generators_path = os.path.join(addon_path, "content_generators")
prefix = "dcg#"


def on_card_will_show(text, card, kind) -> str:
    if kind.startswith("reviewQuestion"):
        return front
    elif kind.startswith("reviewAnswer"):
        return back


# Copy of original code with the addition of the custom "update_card" method
# I would just wrap this method, but I need it to update BEFORE it calls _showQuestion() and AFTER it sets the card
# https://github.com/ankitects/anki/blob/0d8d816a0c424b1e033af7d4d1331816bbb61426/qt/aqt/reviewer.py#L242C1-L258C29
def next_card(self):
    self.previous_card = self.card
    self.card = None
    self._v3 = None
    self._get_next_v3_card()

    self._previous_card_info.set_card(self.previous_card)
    self._card_info.set_card(self.card)

    if not self.card:
        self.mw.moveToState("overview")
        return

    if self._reps is None:
        self._initWeb()

    # -------- Custom Method ---------
    update_card(self.card)
    # --------------------------------

    self._showQuestion()


def get_script_path(card):
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

                return generator_file_path

            # Should only contain one dynamic tag
            break

    except Exception as e:
        showInfo(f"Error processing dynamic content for card {card.id}: {e}")


def get_script_exec_dict(path, exec_dict):
    # Check if script exists
    if os.path.exists(path):
        showInfo(f"Executing script: {path}")

        try:
            with open(path, 'r', encoding='utf-8') as f:
                script_contents = f.read()
                exec(script_contents, exec_dict)

        except Exception as e:
            showInfo(f"Error executing script: {e}")
            raise
    else:
        showInfo(f"Generation script {path} does not exist")


def run_script(exec_dict):
    if 'generate_card' not in exec_dict:
        showInfo("Required method 'generate_card()' not found")
        return

    global front
    global back
    front, back = exec_dict['generate_card']()


def update_card(card):
    script_path = get_script_path(card)

    # Get script dict
    exec_dict = {}
    get_script_exec_dict(script_path, exec_dict)

    # Check if script exists
    if os.path.exists(script_path):
        showInfo(f"Executing script: {script_path}")

        # Attempt to execute script
        run_script(exec_dict)
    else:
        showInfo(f"Generation script {script_path} does not exist")


def main():
    # Generate front and back before card is shown to user
    Reviewer.nextCard = wrap(Reviewer.nextCard, next_card, "before")

    # Change card content
    gui_hooks.card_will_show.append(on_card_will_show)

