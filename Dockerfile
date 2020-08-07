FROM python
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
RUN pip install pycryptodome
WORKDIR /usr/app
ADD main.py flag.py /usr/app/
EXPOSE 12001
CMD [ "python", "main.py" ]
