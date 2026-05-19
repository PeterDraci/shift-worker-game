QUEST_STATES = [
    "activate_computer",
    "restore_power",
    "collect_components",
    "assemble_device",
    "unlock_door",
    "reach_exit",
    "completed"
]

class QuestManager:
    def __init__(self):
        self.current = "activate_computer"
        self.completed = set()

    def advance(self, next_state):
        if next_state in QUEST_STATES:
            self.completed.add(self.current)
            self.current = next_state

    def is_active(self, state):
        return self.current == state
