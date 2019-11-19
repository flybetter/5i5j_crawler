FROM python
COPY . /app
WORKDIR /app
RUN pip install   -i https://pypi.tuna.tsinghua.edu.cn/simple  -r requirements.txt
ENTRYPOINT ["python","-u","/app/stomp_handler.py"]