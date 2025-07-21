from quart import Quart, jsonify, request, render_template
from quart_auth import current_user, QuartAuth
import os
from src.routes import auth_bp, dashboard_bp
from src.db import init_db

app = Quart(__name__)
app.secret_key = 'super-secret-key'

QuartAuth(app)

# add the auth blueprint
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(dashboard_bp, url_prefix='/dashboard')

@app.context_processor
async def inject_user():
    return {"current_user": current_user}

@app.before_serving
async def startup():
    await init_db()

@app.route("/api/videos")
async def videos():
    host = request.host.split(":")[0]  # use the domain without port
    return jsonify([
        {"title": "Live Stream", "url": f"http://{host}:8080/hls/mystream.m3u8"}
    ])


@app.route("/")
async def index():
    stream_key = request.args.get("key", "mystream")
    return await render_template("index.html", stream_key=stream_key)



@app.route("/streams")
async def list_streams():
    hls_dir = "/tmp/hls"
    try:
        files = os.listdir(hls_dir)
        stream_keys = sorted({f.split(".")[0] for f in files if f.endswith(".m3u8")})
        print(stream_keys)

        return jsonify(stream_keys)
    except Exception as e:
        print(e)

        return jsonify([]), 500
