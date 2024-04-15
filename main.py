import sys
from cli import SantoriniCLI

def main():
    if sys.argc > 4:
        print("Usage: python main.py argv1 argv2 argv3 argv4")
    
    # Enable undo/redo
    if sys.argv[3] == 'on':
        SantoriniCLI().run(memento=True)

    else:
        SantoriniCLI().run()