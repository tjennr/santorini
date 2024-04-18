import sys
from cli import SantoriniCLI

if __name__ == '__main__':
    if len(sys.argv) > 4:
        print("Usage: python main.py argv1 argv2 argv3 argv4")
    
    # Enable undo/redo
    if sys.argv[1] == 'human' or sys.argv[1] == 'random' or sys.argv[1] == 'hueristic':
        playerWhite = sys.argv[1]
    else:
        playerWhite = 'human'
    
    if sys.argv[2] == 'human' or sys.argv[2] == 'random' or sys.argv[2] == 'hueristic':
        playerBlue = sys.argv[2]
    else:
        playerBlue = 'human'

    if sys.argv[3] == 'on':
        memento = True
    else:
        memento = False
        
    if sys.argv[4] == 'on':
        score = True
    else:
        score = False

    SantoriniCLI(playerWhite, playerBlue, memento, score).run()