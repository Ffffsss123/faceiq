import os
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename
from utils import load_reference_embedding, get_user_iq_scores_multi

# 配置
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# 启动时加载 IQ140 参考向量
ref_emb = load_reference_embedding("embedding_IQ140.npy")

# 内联 HTML 模板
HTML = '''
<!doctype html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Face IQ Predictor</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body class="p-5">
  <div class="container">
    <h1 class="mb-4">3D检测器-检测你是不是3D! </h1>
    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <input class="form-control" type="file" name="file" accept="image/*" required>
      </div>
      <button class="btn btn-primary" type="submit">上传并预测</button>
    </form>
    {% if results %}
      <hr>
      <h2>预测结果：</h2>
      <img src="{{ url_for('uploaded_file', filename=filename) }}" class="img-fluid mb-3" style="max-width:300px;">
      <ul class="list-group">
        {% for sim, iq, label in results %}
          <li class="list-group-item">
            对比人类智慧学家的相似度 {{ '{:.2%}'.format(sim) }}, 预测 IQ {{ '{:.1f}'.format(iq) }} {% if label %}—— {{ label }}{% endif %}
          </li>
        {% endfor %}
      </ul>
    {% endif %}
  </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    results = None
    filename = None
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(path)
            results = get_user_iq_scores_multi(path, ref_emb)
    return render_template_string(HTML, results=results, filename=filename)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return app.send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run(debug=True)
