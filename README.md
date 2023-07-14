## Requirements
- python 3.9
- redis
- docker
- poetry


## Run on local development

### Run bootstrap
`./bootstrap`

### Run web
`./manage web`

### Run celery (for background task)
`./manage run_celery` 

### Run flower (for background task monitoring)
`./manage run_flower`