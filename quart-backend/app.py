from quart import Quart, jsonify, request, render_template
import os

app = Quart(__name__)


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
