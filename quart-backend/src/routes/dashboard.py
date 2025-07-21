import uuid
from quart import Blueprint, render_template, jsonify
from quart_auth import login_required, current_user
from src.db import get_db
from src.db.models import User
from quart import redirect, url_for, flash
from sqlalchemy.future import select

dashboard_bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@dashboard_bp.route('/')
@login_required
async def dashboard():
    async for db in get_db():
        result = await db.execute(select(User).where(User.id == int(current_user.auth_id)))
        user = result.scalar_one_or_none()

        if not user:
            await flash("User not found", "danger")
            return redirect(url_for("auth.login"))

        return await render_template("dashboard/index.html", stream_key=user.stream_key)


@dashboard_bp.route("/roll-key", methods=["POST"])
@login_required
async def roll_stream_key():
    new_key = uuid.uuid4()

    async for db in get_db():
        result = await db.execute(select(User).where(User.id == int(current_user.auth_id)))
        user = result.scalar_one_or_none()

        if user:
            user.stream_key = str(new_key)
            await db.commit()
            return jsonify({"new_key": new_key})

    return jsonify({"error": "User not found"}), 404
