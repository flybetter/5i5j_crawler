FROM joyzoursky/python-chromedriver:3.6-xvfb-selenium
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python","-u","/app/5i5j.py"]