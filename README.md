# baneks
See `--help` output.
All parameters can also be specified via environment variables.

# message
See `--help` output.

# docker
```
docker build . -t <image name>
docker run --network=host --env USERNAME=<mqtt username> --env PASSWORD=<mqtt password> --env HOST=<mqtt broker address> --env TOPIC=<mqtt topic> <image name>
```
