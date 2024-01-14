# PYTHON.
FROM python:3.9

# Enable Virtual Environment.
ENV VIRTUAL_ENV=/opt/venv
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Upgrade pip, install and upgrade pip dependencies.
COPY docker/pip_install.txt docker/pip_upgrade.txt /code/
WORKDIR /code
RUN python3 -m venv $VIRTUAL_ENV \
    && python -m pip install --upgrade pip \
    && pip install --upgrade pip \
    && pip install -r pip_install.txt \
    && pip install -r pip_upgrade.txt --upgrade \
    && rm -rf /root/.cache/pip

# Copy the app.
COPY . /code