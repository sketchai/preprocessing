# Preprocessing



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


2. Install poetry and package dependencies

1. To install package dependencies with poetry, 

```
    poetry install
```

To update package dependencies, 
```
    poetry update
```

2. Install our gitlab package [FilteringPipeline](https://gitlab.pam-retd.fr/cao_ml/python_packages/abstractfilters/filteringpipeline):
```bash
    pip install -e git+https://gitlab.pleiade.edf.fr/cao_ml/toolbox/filteringpipeline.git#egg=filtering-pipeline
```

3. Install sktechgraphs: to avoid unwanted evolution, use a cloned version on the EDF repo:

```bash
    pip install -e git+https://gitlab.pleiade.edf.fr/cao_ml/sketchgraphs_for_edf/sketchgraphs.git#egg=sketchgraphs
```

Otherwise, use the original github repository:

```bash
    pip install -e git+https://github.com/PrincetonLIPS/SketchGraphs.git@2fbf9e5e84031b233325331c95880a86448e5bee#egg=sketchgraphs
```


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

See test coverage : [TO COMPLETE]


## Preprocessing pipeline 

- [How does the preprocessing pipeline works?](docs/preprocessing.md)
- To launch a coarse-grained pipeline, use the  [following script](config/conf_coarsegrainedpip.yml)


## Good pratices 

### PEP8

Use the pep8 norm to format all the code. Specific pep8 parameters are given into the [pyproject.toml](pyproject.toml) file.

```
autopep8 --in-place --aggressive --aggressive ./
```


### FLAKE8

[TO COMPLETE]
