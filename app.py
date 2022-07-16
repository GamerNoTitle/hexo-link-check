from flask import Flask, send_from_directory, render_template
from flask import request
import os
from utils.HexoLinkCheck import StartCheck

app = Flask(__name__)
@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('./index.html', status='')

@app.route('/js/<path>', methods=['GET', 'POST'])
def js(path):
    return send_from_directory('js', path)

@app.route('/css/<path>', methods=['GET', 'POST'])
def css(path):
    return send_from_directory('css', path)

@app.route('/api/check', methods=['GET', 'POST'])
def check():
    try:
        data = request.get_json()['content']
        domain = data['domain']
        path = data['path']
    except:
        data = request.form.to_dict()
        domain = data['domain']
        path = data['path']
        if domain == None or path == None:
            return {'code': -1, 'msg': 'Invalid parameters.'}
    url = domain + path
    data = StartCheck(url)
    msg = data['msg']
    return render_template('index.html', status=msg)


@app.route('/report', methods=['GET', 'POST'])
def report():
    data = report_api()
    return render_template('report.html', report=data)

@app.route('/api/report', methods=['GET', 'POST'])
def report_api():
    Query = True
    try:
        data = request.get_json()['content']
        domain = data['domain']
    except:
        try:
            domain = request.args.get('domain') if request.args.get('domain') != None else request.form.to_dict()['domain']
            if domain == None:
                return {'code': -1, 'msg': 'Invalid parameters.'}
        except:
            Query = False
    if Query:
        filename = 'hexo-link-check/' + domain.replace('http://', '').replace('https://',
                                                        '').replace('/link', '').replace('/', '')
        try:
            with open(filename, 'r', encoding='utf8') as f:
                content = f.read().split('\n')
            return content
        except:
            return [f'未找到 {domain} 的检查报告！']
    else:
        return ['请在上面输入你的域名进行报告获取！']
if __name__ == '__main__':  # Launcher
    if not os.path.exists('./hexo-link-check'):
        os.mkdir('hexo-link-check')
    # If debug is set to True, every time when the file is saved the program will reload
    app.run(host='0.0.0.0', port=8080, debug=False)
