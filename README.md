# Preprocessing

In this package, we detail how to preprocess data sketches using our SAM data model.

During the preprocessing step, sketches coming from divers CAD sketches sources (here OnShape) are first convert to the SAM data model, then they are filtered based on heuristics.
![CAD_ML_train](https://user-images.githubusercontent.com/103726832/184370818-5f1cb693-0a99-4472-8ed6-a3f317f86e4b.gif)

This preprocessing pipepeline is composed of 6 sub-pipelines:
- a [coarse-grained sub-pipeline](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_coarse.py) that removes graphs based on several criteria (sequence size, number of primitives, etc.)
- a [conversion sub-pipeline](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_convert_sam.py), that converts here OnShape to SAM data model,
- a [normalization sub-pipeline](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_normalization.py), that rescales sketches into a [0,1] X [0,1] box.
- [two clustering sub-pipelines](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_weight.py), that detects and remove duplicate sketches based on the primitives and constraints sequence (first clustering) and on the parameters values (second clustering).
- an [encoding sub-pipeline](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_encoding.py), that converts SAM data model to a specific graph ML model.

To adapt this pipeline to another CAD data model, you must need to:
- write a package to convert from you CAD data model to SAM. You can inspire from [OnShape to SAM package converter](https://github.com/sketchai/sketchgraph_vs_sam),
- update the [conversion pipeline](https://github.com/sketchai/preprocessing/blob/main/experiments/experiment_convert_sam.py).

## Installation

We use conda as an environment manager and poetry as dependency manager.

1. Generate a conda env 
First, create and activate a basic conda env from the [env_prep.yml](./env/env_prep.yml) file. 

Run 
```
    conda env create -f ./env/sg_prep.yml
```

then 

```
    conda activate sg_prep
```

NB: you can change the conda env name in the .yml file if needed



2. To install package dependencies with poetry, 

```
    poetry install
```

At a later stage, if you want to update package dependencies, 
```
    poetry update
```

3. Ensure you have cloned the following repositories:
```bash
    # sketchai local dependencies 
    git clone https://github.com/sketchai/sam
    git clone https://github.com/sketchai/filteringpipeline
    git clone https://github.com/sketchai/sketchgraph_vs_sam

    # sketchgraphs
    git clone https://github.com/PrincetonLIPS/SketchGraphs
```

The recommended way to setup your directory tree is:

```
sketchai
├── filteringpipeline
├── preprocessing
├── sam
├── SketchGraphs
└── sketchgraph_vs_sam
```

4. Install the python packages in editable mode in your conda environment. Ensure your [pip](https://pip.pypa.io/en/stable/getting-started/) version is at least 22.0

```bash
    cd sketchai
    pip install -e ./sam
    pip install -e ./SketchgGraphs
    pip install -e ./sketchgraph_vs_sam
    pip install -e ./filteringpipeline
```

(or use a symlink for the dependencies).

## Testing 

To run all the tests:

```
    poetry run pytest 
```

To run a specific test: 
```
    poetry run pytest path/my_test
```

We use a small 5 sequence long dataset extracted from the sg_t16_test.npy file to do the testing. It is located under tests/asset/sg_t16_mini.npy

All integration tests will not pass on first run, in that case run pytest again 3 or 4 times.



## Preprocessing pipeline 


An easy way to change the paths to your data folder is to use the following symbolic link (on linux).

```sh
ln -s path/to/your/data/folder data
```

The corresponding folder should contain the `sg_t16_train` `test` and `validation.npy` files.
Otherwise make sure to configure the correct paths to the sketchgraphs dataset in the `config/global.yml` file

In order to properly split the dataset, files must be merged first by running

```sh
python experiments/merge_dataset.py
```

Launch script on your pc
```sh
# to run the complete pipeline on validation (ETA: ~20min)
python experiments/full_pipeline.py --dataset validation

# Run the complete pipeline on all data (ETA: ~7hours)
python experiments/full_pipeline.py --dataset merged

# or run only one specific step
python experiments/experiment_coarse.py 
python experiments/experiment_convert_exchangeformat.py 
python experiments/experiment_normalization.py 
python experiments/experiment_weight.py 
python experiments/experiment_encoding.py

# Split between train test and val
python experiments/split_dataset.py

# Save params
python experiments/preprocessing_params.py
```

## Good pratices 

### PEP8

Use the pep8 norm to format all the code. Specific pep8 parameters are given into the [pyproject.toml](pyproject.toml) file.

```
autopep8 --in-place --aggressive --aggressive ./
```



