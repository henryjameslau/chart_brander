from flask import Flask, request, send_file
from flask import render_template

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from io import BytesIO

import time
import base64

app = Flask(__name__)

@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    # response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate,post-check=0, pre-check=0, max-age=0'
    return response

@app.route('/')
def index():
    template = 'index.html'
    return render_template(template)

@app.route('/branding')
def branding():
    template = 'branding.html'
    return render_template(template)

@app.route('/test')
def test():
    template = 'test.html'
    return render_template(template)

@app.route('/chart', methods=['POST', 'GET'])
def chart():
    def serve_pil_image(pil_img):
        img_io = BytesIO()
        pil_img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')

    template = 'chart.html'
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1980,1980")
    chrome_options.add_argument("--hide-scrollbars")

    driver = webdriver.Chrome(chrome_options=chrome_options)



    if request.method=='POST':

        title=request.form['title']
        link=request.form['url']
        source=request.form['source']
        # path=request.form['path']
        # print(title,link,source,path)
        driver.get('http://localhost:5000/branding')
        time.sleep(1)

        title_input = driver.find_element_by_id("change-title")
        link_input = driver.find_element_by_id("change-link")
        source_input = driver.find_element_by_id("change-source")
        # path_input = driver.find_element_by_id("change-path")

        title_input.send_keys(title)
        time.sleep(0.1)
        link_input.send_keys(link)
        time.sleep(0.1)
        source_input.send_keys(source)
        time.sleep(0.1)
        # path_input.send_keys(path)
        driver.find_element_by_id("submit-title").click()
        time.sleep(1)

        element = driver.find_element_by_id('viz')

        location = element.location
        size = element.size

        png=driver.get_screenshot_as_png()
        driver.quit()

        x = location['x']
        print(x)
        y = location['y']
        print(y)
        w = size['width']
        print(w)
        h = size['height']
        print(h)
        width = x + w
        height = y + h


        im = Image.open(BytesIO(png))

        im = im.crop((int(x), int(y), int(width), int(height)))
        # im.save(path + 'image.png')

        # image = request.files[path]
        #
        # image_64_encode = base64.encodestring(im)
        var_dict = {'screenshot': im}
        print(var_dict)
        # img_io = BytesIO()
        # im.save(img_io,'PNG')
        # img_io.seek(0)
        # return send_file(img_io, mimetype='image/png')

        # driver.quit()
        return serve_pil_image(im)
    else:
        return 'nothing'


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
