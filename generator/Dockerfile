FROM python:3.12
MAINTAINER RuslanKhaliullin
WORKDIR /app
COPY requirenments.txt .
RUN pip install --no-cache-dir -r requirenments.txt
COPY generate.py .
EXPOSE 8050
CMD ["python", "/app/generate.py"]