import sys, getopt, os
from Bio import SeqIO
from Bio.Blast import NCBIXML

gbk_filename = "A909_ATCC.gbk"
input_file = open(gbk_filename, "r")

def main(argv):
    gbk_filename = ''

    opts, args = getopt.getopt(sys.argv[1:],"hg:",["help","gbkfile="])
    for opt, arg in opts:
      if opt == '-h':
        print ('gbktofsas.py -g <gbk>')
        sys.exit()
      elif opt in ("-g", "--gbk"):
        gbk_filename = arg
         
    print ('Genebank file is ', gbk_filename)

    with open(gbk_filename, 'r') as input_file:
        try:
            for seq_record in SeqIO.parse(input_file, "genbank") :
                print("GenBank record %s" % seq_record.id)
                for seq_feature in seq_record.features :
                    if seq_feature.type=="CDS":
                        if seq_feature.qualifiers.get('translation') != None:
                            with open('proteins/' + seq_feature.qualifiers['locus_tag'][0] + '.fasta', 'a') as save_file:
                                save_file.write('>' + seq_feature.qualifiers['locus_tag'][0] + '\n')
                                save_file.write(''.join(seq_feature.qualifiers['translation']) + '\n')
        finally:
            input_file.close()

if __name__ == "__main__":
   main(sys.argv[1:])
