# built in library
from pprint import pformat

# external libraries
from sanic import Sanic
from sanic.response import html, redirect, text, json
from jinja2 import Environment, PackageLoader
import pandas as pd

# own
import measures as ms
import util


env = Environment(
    loader=PackageLoader("app", "templates"),
)

DATAFRAME = pd.DataFrame()

app = Sanic(__name__)
app.static("/static", "./static")


@app.route("/")
async def root(request):
    return redirect(app.url_for('home'))


@app.route("/home")
async def home(request):
    template = env.get_template("home.html")
    html_content = template.render()
    return html(html_content)


@app.route("/input", methods=['POST', 'GET'])
async def input(request):
    file = request.files.get('selectedFile')
    try:
        content0 = util.read_excel_from_request(file.body)
        content = [(row[0], row[1:]) for row in content0]
    except Exception as e:
        raise e
        content = []

    template = env.get_template("input.html")
    html_content = template.render(
        uploaded=content, measure_labels=ms.labels)
    return html(html_content)


@app.route("input/show", methods=['POST'])
async def show(request):
    reqform = request.form
    if 'names' not in reqform or 'values' not in reqform:
        template = env.get_template("error.html")
        html_content = template.render(error_message="No data :S")
        return html(html_content)

    data = util.to_dict(reqform['names'], reqform['values'])
    matrix = util.do(data, reqform['measure'][0])
    subjects = data.keys()
    DATAFRAME = pd.DataFrame(data=matrix, index=subjects, columns=subjects)
    DATAFRAME.to_excel("static/files/generated.xlsx")
    template = env.get_template("display.html")
    html_content = template.render(
        download=1,
        measure_type=ms.labels[reqform['measure'][0]],
        keys=subjects, matrix=zip(subjects, matrix))
    return html(html_content)


if __name__ == "__main__":
    app.run(
        debug=True,
        host="localhost",
        port=8000
    )
