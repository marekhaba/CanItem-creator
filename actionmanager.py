"""
Manages all the actions and undo redo,
use:\n
ActionManager.undo() \n
ActionManager.redo() \n
ActionManager.create_action(name, info, undo, redo):\n
    name - genric name of the thing thats happening
    info - more spesific information about what happened
    undo - command that when is called undoes the action
    redo - command that repeats(redoes) the action
    should be a lambda it's better to create a function for creating the lambda due to python's "pass by object reference"
"""

class _Action:
    """
    Represents an action that was conducted.
    Used for undo redo
    undo and redo should be functions.
    """
    def __init__(self, name, info, undo, redo):
        self.name = name
        self.info = info
        self.undo = undo
        self.redo = redo

class _ActionManager:
    """
    Used to manage all action and the undo and redu stuff
    """
    def __init__(self):
        self.actions = []
        self.curent_action = 0
    
    def undo(self):
        if abs(self.curent_action) < len(self.actions):
            self.curent_action -= 1
            #print(self.actions[self.curent_action].info)
            self.actions[self.curent_action].undo()

    def redo(self):
        if self.curent_action < 0:
            #print(self.actions[self.curent_action].info)
            self.actions[self.curent_action].redo()
            self.curent_action +=1

    def create_action(self, name, info, undo, redo):
        """
        Creates an action object for undo redo system\n
        name - genric name of the thing thats happening\n
        info - more spesific information about what happened\n
        undo - command that when is called undoes the action\n
        redo - command that repeats(redoes) the action\n
        for undo and redo use create_lambda to create the function
        """
        self.actions = self.actions[:len(self.actions)+self.curent_action]
        self.actions.append(_Action(name, info, undo, redo))
        self.curent_action = 0

ActionManager = _ActionManager()
