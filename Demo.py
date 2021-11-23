import RegExPy as REP
import sys

def main():
  argsList = sys.argv
  string, regex = argsList[1], argsList[2]   
  print(REP.isMatch(string, regex))
  
if __name__ == "__main__":
  main()