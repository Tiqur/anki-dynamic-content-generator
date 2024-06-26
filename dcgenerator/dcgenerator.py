from aqt import gui_hooks
from aqt.utils import showInfo

def show_tags_before_question(card):
    # Get tags associated with the current card
    tags = card.note().tags

    # Display the tags
    showInfo(f"Tags for next card: {', '.join(tags)}")

gui_hooks.reviewer_did_show_question.append(show_tags_before_question)


