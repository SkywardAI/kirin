# Development methods

There are two ways to do development:


## Development outside docker

You can't debug step by step in this mode. However, your changed will be deployed automatically by docker compose.

First, please run `make up`, and then use `make log` to stream output logs to the terminal.

Second, edit code with your IDE. And the code will automatically build and run. You can check from the `<deployment-ip>:80` to check the code.


## Development with Devcontainer

For developer, we encourage you to use the following technologies. You can debug step by step and don't need to care about other components' containers.

* VSCode
* Devcontainer

There are one step to start the development environment:

. Open the project in VSCode and click on the `Reopen in Container` button or open the current folder in a container.

And VSCode will automatically build the development environment based on our [pre-build images](https://hub.docker.com/r/gclub/skywardai/tags).

And you can check the swagger UI on `<deployment-ip>:8000/docs/`


Happy coding!
