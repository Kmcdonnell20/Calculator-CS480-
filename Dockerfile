From python:3.8

WORKDIR ./app

COPY . /app

RUN pip install streamlit==1.1.0

EXPOSE 8501

CMD streamlit run main.py