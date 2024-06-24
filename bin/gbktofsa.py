import sys, getopt, os
from Bio import SeqIO
from Bio.Blast import NCBIXML

def main(argv):
    gbk_filename = ''
    outputfile = ''

    opts, args = getopt.getopt(sys.argv[1:],"hg:o:",["help","gbkfile=","outputfile="])
    for opt, arg in opts:
      if opt == '-h':
        print ('gbktofsa.py -g <gbk> -o <output>')
        sys.exit()
      elif opt in ("-g", "--gbk"):
        gbk_filename = arg
      elif opt in ("-o", "--output"):
        outputfile = arg
         
    print ('Genebank file is ', gbk_filename)
    print ('Output file is ', outputfile)
   
    with open(gbk_filename, 'r') as input_file:
        try:
            for seq_record in SeqIO.parse(input_file, "genbank") :
                print("GenBank record %s" % seq_record.id)
                for seq_feature in seq_record.features :
                    if seq_feature.type=="CDS":
                        if seq_feature.qualifiers.get('translation') != None:
                            with open(outputfile, 'a') as save_file:
                                try:
                                    save_file.write('>' + seq_feature.qualifiers['locus_tag'][0] + '\n')
                                    save_file.write(''.join(seq_feature.qualifiers['translation']) + '\n')
                                finally:
                                    save_file.close()
        finally:
            input_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])