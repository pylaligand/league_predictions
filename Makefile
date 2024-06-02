.PHONY: fetch
fetch:
	PYTHONPATH=. tools/fetch_games.py $(ARGS)

.PHONY: app
app:
	streamlit run app/main.py

.PHONY: test
test:
	python -m unittest discover modules/

.PHONY: docker-build
docker-build:
	docker build -t promoracle:local .

.PHONY: docker-run
docker-run: docker-build
	docker run --rm -p 8501:8501 promoracle:local

.PHONY: clean
clean:
	docker image prune -a -f
	docker container prune -f
