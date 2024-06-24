# ScanDis
Tool for using DrBert and TMbed to find protein features across genomes.

## Required Pre-Installations
* [TMbed](https://github.com/BernhoferM/TMbed "TMBed Github Repository")
* [DR-BERT](https://github.com/maslov-group/DR-BERT "DR-BERT Github Repostiroy")

Reference each github for specific installation instructions, ensuring to create a separate conda environment for each package. Sample environment files are provided for running both under Ubuntu 23.04.

Create an environment for each tool by using the `drbert.yml` or `tmbed.yml` file that via
```shell
conda env create -f environments/drbert.yml
```

However, these depending on the specifics of your particular installation environment, changes might need to be made to the individual environments.


## Configuring Script
Once you have both tools installed, edit scandis.sh to reflect your installation path for DR-BERT.

```shell
### Path to DR-BERT Install
BERT_PATH=/home/$USER/archive/DR-BERT
```

You may also wish to edit the specific GPU(s) that will be used. If you don't know the specific device ID, you type ```nvidia-smi``` to enumerate your installed devices. Then uncomment and edit the line to include only devices you want the script to see.

```shell
export CUDA_VISIBLE_DEVICES=0,1
```

## Running a Job
ScanDis takes a genome in Genbank record format as input. Running a job is as simple as invoking the script from the ScanDis directory.

```shell
./scandis.sh genome.gbk
```