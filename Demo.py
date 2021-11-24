from RegExPy import RegexCompiler
import sys

def main():
  argsList = sys.argv
  string, regex = argsList[1], argsList[2] 
  regexer = RegexCompiler(regex)
  print(regexer.isMatch(string))
  print(regexer.matches(string))
if __name__ == "__main__":
  main()