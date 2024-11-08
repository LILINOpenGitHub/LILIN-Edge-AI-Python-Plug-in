import sys
import codecs

def PrintHelloWorld():
    print("Hello World!")
if __name__ == '__main__':
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach()) # avoiding UnicodeEncodeError in HTML file
    PrintHelloWorld()
