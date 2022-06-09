# Preprocessing

In this package, we detail how to preprocess data sketches using our SAM data model.


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

NB: it can be good to change the conda name env into [env_basic_conda.yml](./env/env_basic_conda.yml) file.



2. To install package dependencies with poetry, 

```
    poetry install
```

To update package dependencies, 
```
    poetry update
```

3. Ensure you have cloned the following repositories somewhere:
```bash
    # sketchai local dependencies 
    git clone https://github.com/sketchai/sam
    git clone https://github.com/sketchai/filteringpipeline
    git clone https://github.com/sketchai/sketchgraph_vs_sam

    # sketchgraphs
    git clone https://github.com/PrincetonLIPS/SketchGraphs
```

4. Install packages in editable mode (latest version of pip is required)

```bash
    # for each package run
    pip install -e path/to/your/package
```
(or use a symlink for the dependencies).

## Testing 

For running all the tests:

```
    poetry run pytest 
```

For running a specific test: 
```
    poetry run pytest path/my_test
```

We use a small 5 sequence long dataset extracted from the sg_t16_test.npy file to do the testing. It is located under tests/asset/sg_t16_mini.npy

All integration tests may not pass on first run, in that case run pytest again.



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
# to run the complete pipeline
python experiments/full_pipeline.py 

# or run only one specific step
python experiments/experiment_coarse.py 
python experiments/experiment_convert_exchangeformat.py 
python experiments/experiment_normalization.py 
python experiments/experiment_weight.py 
python experiments/experiment_encoding.py

# Split btw train test and val
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



