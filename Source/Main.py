# Makes Electron work
import sys
import os

sys.path.append(os.path.dirname(__file__))

# Actual main logic

from Core import Core


# Main function
def main():
    print("Hello world!")
    core : Core = Core()

if __name__ == "__main__":
    main()