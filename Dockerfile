FROM python:3.6
ARG project_dir=/src/
ADD src/requirements.txt ${project_dir}
WORKDIR ${project_dir}

ARG DB_USERNAME=${DB_USERNAME}
ENV DB_USERNAME ${DB_USERNAME}
ARG DB_PASSWORD=${DB_PASSWORD}
ENV DB_PASSWORD ${DB_PASSWORD}
ARG DB_HOST=${DB_HOST}
ENV DB_HOST ${DB_HOST}
ARG DB_NAME=${DB_NAME}
ENV DB_NAME ${DB_NAME}
ENV MAPS_API_KEY ${MAPS_API_KEY}

RUN pip install numpy
RUN pip install -r requirements.txt
RUN pip install spacy[ja]

COPY src/ /src/

CMD flask run --host 0.0.0.0 --port 8080 --reload
