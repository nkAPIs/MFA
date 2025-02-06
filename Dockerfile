# Using Python-image
FROM python:3.12-slim

# Set workdirectory
WORKDIR ./

EXPOSE 8000

# Install dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    libpq-dev gcc && \
    rm -rf /var/lib/apt/lists/*

# Upgrading pip
RUN pip install --upgrade pip

# Copying files
COPY . .

# Manually installing psycopg2
RUN pip install psycopg2==2.9.10

# Manually install nkdatabase-wheel
RUN pip install ./custom_modules/nkdatabase-1.0.2-py3-none-any.whl

# Running pip install on req.txt
RUN pip install -r requirements.txt

CMD ["fastapi", "run", "mfaAPI.py", "--port", "8000"]