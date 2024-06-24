import sys, getopt, os
import csv
from itertools import tee, islice, chain
import pickle
import numpy as np

def previous_and_next(some_iterable):
    prevs, items, nexts = tee(some_iterable, 3)
    prevs = chain([None], prevs)
    nexts = chain(islice(nexts, 1, None), [None])
    return zip(prevs, items, nexts)

def main(argv):
    pklfile = ''
    outputfile = ''
    opts, args = getopt.getopt(sys.argv[1:],"hp:o:",["help","pklfile=","outputfile="])
    for opt, arg in opts:
      if opt == '-h':
        print ('parse_disorder.py -p <pkl> -o <output>')
        sys.exit()
      elif opt in ("-p", "--pkl"):
        pklfile = arg
      elif opt in ("-o", "--output"):
        outputfile = arg
         
    print ('PKL file is ', pklfile)
    print ('Output file is ', outputfile)
   
    with open(pklfile, 'rb') as reader:
      try:
        df = pickle.load(reader)
        with open(outputfile, 'w') as writer:
          try:
            for index, row in df.iterrows():
              writer.write(">" + row['ID'] + "\n")
              writer.write(row['sequence'] + "\n")
              for score in row['score']:
                if score < 0.5:
                  writer.write('.')
                elif score < 0.75:
                  writer.write('d')
                else:
                  writer.write('D')
              writer.write("\n")
          finally:
            writer.close()
      finally:
        reader.close()
        
if __name__ == "__main__":
   main(sys.argv[1:])