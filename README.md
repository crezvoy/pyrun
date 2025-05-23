# pyrun

Pyrun is a service that allows isolated execution of python scripts through nsjail

## Trying pyrun locally

Start a local instance of pyrun 
``` sh
make run
```

``` sh
curl -X POST localhost:8080/execute \
  -H "Content-Type: application/json" \
  -d '{"script":"def main():\n    return \"{ \\\"output\\\": \\\"Hello, World}\\\" }\"\n"}'
```

## Deployment to Google cloud run

Create an `.env` file following the `.env.template` provided and run the following commands

``` sh
make login
make deploy
```

