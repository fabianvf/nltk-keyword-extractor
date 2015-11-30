from invoke import task


@task
def extract(text=None, filename=None):
    from extract import main
    if filename:
        with open(filename) as f:
            text = f.read()
    print(main(text))
