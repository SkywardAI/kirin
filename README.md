<h1 align=center><strong>Kirin</strong></h1>

[![Linter and Builder 🚀](https://github.com/SkywardAI/chat-backend/actions/workflows/linter-and-builder.yaml/badge.svg)](https://github.com/SkywardAI/chat-backend/actions/workflows/linter-and-builder.yaml) [![Release Drafter 🚀](https://github.com/SkywardAI/chat-backend/actions/workflows/release-drafter.yml/badge.svg)](https://github.com/SkywardAI/chat-backend/actions/workflows/release-drafter.yml) [![Releasing Image 🚀](https://github.com/SkywardAI/kirin/actions/workflows/release-image.yaml/badge.svg)](https://github.com/SkywardAI/kirin/actions/workflows/release-image.yaml) [![CodeQL](https://github.com/SkywardAI/kirin/actions/workflows/github-code-scanning/codeql/badge.svg)](https://github.com/SkywardAI/kirin/actions/workflows/github-code-scanning/codeql)


# Architecture

![](./imgs/SkywardAI(Mind%20Map)%20-%20APIs%20aggregator.svg)


# Doing inference on 8 CPUs

https://github.com/SkywardAI/kirin/assets/8053949/143b016c-2264-4644-a7ae-304c908fbedf


# Features

- [x] **Inference mode(default)**: Chat with the small language model at consumer grade hardware with 8 CPUs
- [x] **RAG mode**: Chat with small language model based on pre-processed datasets
- [x] **CRM feature**s: Multiple users login, chat/chat(RAG), save chat history and share the chat history by JSON format
- [ ] **Neural Network define**
     - [ ] Pre-define neural network as template, support load weights and fine-tune
     - [ ] Support multiple neural network types
     - [ ] Support custom simple neural network by UI

- [ ] **Training Factory**
     - [ ] Train the neural network with the given dataset  
     - [ ] Quantize the model and upload it to the server with the given tokens  
     - [ ] Visualize the neural network and the training process
 
# Requirements

See [Requirements.md](./docs/Requirements.md)


# Quick setup

See [quick start](https://skywardai.github.io/skywardai.io/docs/quick-start.html)


# Tech stack

This is a repository is the API aggregator of SkywardAI. It's using the following tech stack:

* 🐳 [Dockerized](https://www.docker.com/)
* 🐘 [Asynchronous PostgreSQL](https://www.postgresql.org/docs/current/libpq-async.html)
* 🐍 [FastAPI](https://fastapi.tiangolo.com/)

When the `Docker` is started, these are the URL addresses:

* Backend Application (API docs) $\rightarrow$ `http://localhost:8000/docs`
* Database editor (Adminer) $\rightarrow$ `http//localhost:8081`

## Why the above Tech-Stack?

Well, the easy answer is **Asynchronousity** and **Speed**!

* **FastAPI** is crowned as the fastest web framework for Python and thus we use it for our backend development.
* The database of my choice is the **asynchronous** version of **PostgreSQL** (via [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html)). Read [this blog from Packt](https://subscription.packtpub.com/book/programming/9781838821135/6/ch06lvl1sec32/synchronous-asynchronous-and-threaded-execution) if you want to educate yourself further about the topic **Asynchronous, Synchronous, Concurrency,** and **Parallelism**.
* **Docker** is a technology that packages an application into standardized units called containers that have everything the software needs to run including libraries, system tools, code, and runtime.


## Other Technologies

The above-listed technologies are just the main ones. There are other technologies utilized in this project template to ensure that your application is robust and provides the best possible development environment for your team! These technologies are:

* [CodeCov](https://about.codecov.io/) $\rightarrow$ A platform that analyzes the result of your automated tests.
* [PyTest](https://docs.pytest.org/en/7.2.x/) $\rightarrow$ The testing framework for Python code.
* [DBDiagram](https://dbdiagram.io/home) $\rightarrow$ A platform that lets your design your database by writing SQL and converting it into ERD. This platform provides a complete symbol for entity relationships (not like many other platforms!).
* [GitHub Actions](https://github.com/features/actions) $\rightarrow$ The platform to setup our CI/CD by GitHub.
* [SQLAlchemy 2.0](https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html) $\rightarrow$ The go-to database interface library for Python. The 2.0 is the most recent update where it provides an asynchronous setup.
* [CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners) $\rightarrow$ A file for distributing the responsibilities in our project to each team/teammate.


# Build and deployment

<!-- https://stackoverflow.com/questions/2068344/how-do-i-get-a-youtube-video-thumbnail-from-the-youtube-api -->

[![Build and Deployment](https://img.youtube.com/vi/63OxSmcBkhI/0.jpg)](https://youtu.be/63OxSmcBkhI?si=G82BOtcwRvQE7dLU)

Also See [deployment](https://skywardai.github.io/skywardai.io/docs/development/build_and_run.html). And if you are interested in docker-in-docker development, see [Development.md](./docs/Development.md)


## Acknowledgements

* [FastAPI](https://fastapi.tiangolo.com/)
* [SQLAlchemy](https://www.sqlalchemy.org/)
* [llama.cpp](https://github.com/ggerganov/llama.cpp)
* [HuggingFace](https://huggingface.co)
* [RMIT Race Hub](https://race.rmit.edu.au)
* [Microsoft Phi-3 Series](https://huggingface.co/aisuko/Phi-3-mini-4k-instruct-gguf)


# LICENSE

This project is licensed under the terms of the Apache 2.0 license. See the [LICENSE](./LICENSE.md) file.
