FROM quay.io/astronomer/ap-airflow:2.1.0-buster-onbuild


# Ensure Pip is up-to-date
RUN pip3 install --upgrade pip --user