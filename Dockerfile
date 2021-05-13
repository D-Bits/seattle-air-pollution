FROM quay.io/astronomer/ap-airflow:2.0.2-buster-onbuild


# Ensure Pip is up-to-date
RUN pip3 install --upgrade pip --user