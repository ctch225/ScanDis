#!/bin/bash
export CUBLAS_WORKSPACE_CONFIG=:4096:8
export CUDA_VISIBLE_DEVICES=0

### Path to DR-BERT Install
BERT_PATH=/home/$USER/archive/DR-BERT

### get script directory
BIN=$(dirname "${BASH_SOURCE[0]}")
pushd $BIN > /dev/null
popd > /dev/null

if [ -z "$1" ]
  then
    echo "No argument supplied"
    exit
fi

### set input and output directories
GENOME=`pwd`
PROTEINS=${GENOME}/proteins
MODELS=${GENOME}/models
files=(${PROTEINS}/*.fasta)

mkdir -p $PROTEINS
mkdir -p $MODELS

### parse input for filename components
filename=$(basename -- "$1")
extension="${filename##*.}"
GENOME_NAME="${filename%.*}"

### convert genebank to fasta format if necessary
if [[ $extension == gbk ]]
    then
        python bin/gbktofsa.py -g $filename -o ${GENOME_NAME}.fasta
    else
        echo Error: Please provide a file in the Genebank file format ending in .gbk
        exit 1
fi

### create individual protein fasta files
python bin/gbktofsas.py -g $filename

eval "$(conda shell.bash hook)"

for ((i = 0; i < ${#files[@]}; i++)); do
    SUFFIX=`echo ${files[i]} | awk -F . '{print $NF}'`
    ID1=`basename ${files[i]%.$SUFFIX}`
    
    if [ ! -f $MODELS/${ID1}/${ID1}.scan ]
    then
        conda activate tmbed
        python -m tmbed predict -f $PROTEINS/${ID1}.fasta -p $MODELS/${ID1}/protein.pred --use-gpu --no-cpu-fallback
        conda deactivate
    fi
done

cat $MODELS/*/protein.pred > $GENOME/$GENOME_NAME.pred

conda activate drbert
python $BERT_PATH/get_scores_fasta.py $BERT_PATH/checkpoint-final/ $GENOME/$GENOME_NAME.fasta $GENOME/$GENOME_NAME.pkl
conda deactivate

python $GENOME/bin/parse_disorder.py -p $GENOME/$GENOME_NAME.pkl -o $GENOME/${GENOME_NAME}_DRBERT_DISORDER.pred
python $GENOME/bin/pred_transmembrane.py -p $GENOME/$GENOME_NAME.pred -o $GENOME/${GENOME_NAME}_TRANS.txt
python $GENOME/bin/pred_signal.py -p $GENOME/$GENOME_NAME.pred -o $GENOME/${GENOME_NAME}_SIGNAL.txt
python $GENOME/bin/pred_disordered.py -p $GENOME/${GENOME_NAME}_DRBERT_DISORDER.pred -o $GENOME/${GENOME_NAME}_DRBERT_DISORDER.txt