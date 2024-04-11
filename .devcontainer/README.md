# Using a Dev Container in VS Code

The Visual Studio Code Dev Containers extension lets you use a container as a full-featured development environment.
It allows you to open any folder inside (or mounted into) a container and take advantage of Visual Studio Code's full feature set.

![image](https://code.visualstudio.com/assets/docs/devcontainers/containers/architecture-containers.png)

## Requirements

- [ ] Docker installed locally.
- [ ] VS Code Dev Containers Extension.

  - Name: Dev Containers
  - Id: ms-vscode-remote.remote-containers
  - Description: Open any folder or repository inside a Docker container and take advantage of Visual Studio Code's full feature set.
  - Version: 0.347.0
  - Publisher: Microsoft
  - [VS Marketplace Link](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers)

  Extension Image:

  ![image](https://github.com/kevinknights29/Python-Dev-Container-Template/assets/74464814/ab61365f-ce34-4804-96d1-ebacac052db9)

For more, please refer to: [System Requirements](https://code.visualstudio.com/docs/devcontainers/containers#_system-requirements)

## Usage

If you meet the requirements, you can get started by just opening this project in VS Code, and selecting `Open in Dev Container`.

If the message above doesn't appear, you can press `ctrl + shift + p` on your keyboard and type: `dev container`. Select: `Open in Dev Container`.

This should display a status bar like the example below:

![image](https://code.visualstudio.com/assets/docs/devcontainers/containers/dev-container-progress.png)

The build process would look like the example below:

![image](https://github.com/kevinknights29/Python-Dev-Container-Template/assets/74464814/fda40919-f4f8-4ec4-8a07-71c0fd185363)

After the container starts successfully, you are ready to use and add features to the code.

## Resources

For a more in-depth guide, please refer to:

- [Setting a Dockerized Python Development Environment Template
](https://medium.com/@rami.krispin/setting-a-dockerized-python-development-environment-template-de2400c4812b)
- [A Dockerized Python Development Environment Template
](https://github.com/RamiKrispin/vscode-python-template?source=post_page-----de2400c4812b--------------------------------)
