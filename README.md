## Requirements
- python 3.9 | *we recommended to use* [pyenv](https://github.com/pyenv/pyenv) *for python versioning manager*
- redis 6
- docker
- poetry

### Cuda Requirements
[nvidia cuda versioning reference](https://www.tensorflow.org/install/source#gpu)
| name          | version | reference                                                                      |
| :------------ |:-------:| :------------------------------------------------------------------------------|
| cuda-toolkit  | 11.7    | [cuda-toolkit-archive](https://developer.nvidia.com/cuda-toolkit-archive)      |
| cudnn         | 8.6     | [cudn-archieve](https://developer.nvidia.com/rdp/cudnn-archive)                |
| nvidia nccl   | 11.0    | [nccl-legacy-archieve](https://developer.nvidia.com/nccl/nccl-legacy-downloads)|

**Note:**

```
cuda version should be satisfied with your gpu device
In this reference, it's use gpu device **gtx 1660 turing**
```

## Run on local development

### Run bootstrap

should be run redis on docker

`./bootstrap`

### Run web
`./manage web`
[Web local dev port 5002](http://localhost:5002)

### Run celery (for background task)
`./manage run_celery` 

### Run flower (for background task monitoring)
`./manage run_flower`
[Flower local dev port 5555](http://localhost:5555)