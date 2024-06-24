import sys, getopt, os
import csv
from itertools import tee, islice, chain

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

def main(argv):
    predfile = ''
    outputfile = ''
    opts, args = getopt.getopt(sys.argv[1:],"hp:o:",["help","predfile=","outputfile="])
    for opt, arg in opts:
      if opt == '-h':
        print ('pred_disordered.py -p <pred> -o <output>')
        sys.exit()
      elif opt in ("-p", "--pred"):
        predfile = arg
      elif opt in ("-o", "--output"):
        outputfile = arg
         
    print ('Pred file is ', predfile)
    print ('Output file is ', outputfile)
   
    with open(predfile, 'r') as predreader:
      try:
        with open(outputfile, 'w') as writer:
          try:
            predictions = predreader.readlines()
            for prev, prediction, nxt in previous_and_next(predictions):
              if str(prev).startswith(">"):
                if "D" in nxt:
                  writer.write(prev)
          finally:
            writer.close()
      finally:
        predreader.close()
        
if __name__ == "__main__":
   main(sys.argv[1:])