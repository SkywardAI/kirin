# Requirements

The requirements development tools see below:

```bash
sudo apt install docker.io
sudo apt install docker-compose-v2
```

## Docker series

```bash
ubuntu:~$ docker version
Client:
 Version:           24.0.7
 API version:       1.43
 Go version:        go1.21.1
 Git commit:        24.0.7-0ubuntu2~22.04.1
 Built:             Wed Mar 13 20:23:54 2024
 OS/Arch:           linux/amd64
 Context:           default

Server:
 Engine:
  Version:          24.0.7
  API version:      1.43 (minimum version 1.12)
  Go version:       go1.21.1
  Git commit:       24.0.7-0ubuntu2~22.04.1
  Built:            Wed Mar 13 20:23:54 2024
  OS/Arch:          linux/amd64
  Experimental:     false
 containerd:
  Version:          1.7.12
  GitCommit:        
 runc:
  Version:          1.1.12-0ubuntu2~22.04.1
  GitCommit:        
 docker-init:
  Version:          0.19.0
  GitCommit:

####################################################
ubuntu:~/workspace/aisuko/kirin$ docker compose version
Docker Compose version 2.24.6+ds1-0ubuntu1~22.04.1
```

## Rootless docker

```
ec2-user@ip-10-110-144-85:~/workspace/kirin$ sudo usermod -aG docker $USER
ec2-user@ip-10-110-144-85:~/workspace/kirin$ newgrp docker

ec2-user@ip-10-110-144-85:~/workspace/kirin$ docker ps -a
CONTAINER ID   IMAGE     COMMAND   CREATED   STATUS    PORTS     NAMES
```

And you are good to go.