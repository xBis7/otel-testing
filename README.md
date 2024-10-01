## Setup

### Initialize the submodules

```bash
git submodule init
git submodule update
```

### Jenkins

We can conditionally check if we need to run jenkins from a war file but we have to copy it in any case. It needs to be available.

Generate the war file

```bash
./utils/get_custom_jenkins_war.sh /path/to/projects
```

### Airflow

Build all images

```bash
./utils/build_airflow.sh /path/to/projects
```
