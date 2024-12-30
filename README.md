
All scripts should be executed from the project root.

## jenkins-airflow

### Jenkins

We can conditionally check if we need to run jenkins from a war file but we have to copy it in any case. It needs to be available.

Generate the war file

```bash
./jenkins-airflow/utils/get_custom_jenkins_war.sh /path/to/projects
```

### Airflow

Build all images

```bash
./jenkins-airflow/utils/build_airflow.sh /path/to/projects
```

## partial-spans


