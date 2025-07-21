from quart import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import check_password_hash, generate_password_hash
import asyncio
from quart_auth import login_user, AuthUser, login_required
from src.db import get_db
from src.db.models import User
from sqlalchemy import select

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
async def login():
    if request.method == 'POST':
        form = await request.form
        email = form.get('email')
        password = form.get('password')

        user = None
        async for db in get_db():
            stmt = select(User).where(User.email == email)
            result = await db.execute(stmt)
            user = result.scalars().first()

        if not user:
            await flash("Invalid email or password", "danger")
            return redirect(url_for('auth.login'))

        valid = await asyncio.to_thread(check_password_hash, user.password, password)
        if valid:
            login_user(AuthUser(str(user.id)))
            return redirect(url_for('index'))

        await flash("Invalid email or password", "danger")
        return redirect(url_for('auth.login'))

    return await render_template('auth/login.html')


@auth_bp.route('/signup', methods=['GET', 'POST'])
async def signup():
    if request.method == 'POST':
        form = await request.form
        email = form.get('email')
        password = form.get('password')
        confirm_password = form.get('confirm_password')

        print(f"Received signup request with email: {email}")

        if not password or password != confirm_password:
            await flash("Passwords do not match", "danger")
            return redirect(url_for('auth.signup'))

        async for db in get_db():
            # Check if user already exists
            result = await db.execute(select(User).where(User.email == email))
            existing_user = result.scalar()

            if existing_user:
                await flash("An account with that email already exists.", "danger")
                return redirect(url_for('auth.signup'))

            # Create and add new user
            hashed_password = await asyncio.to_thread(generate_password_hash, password)
            new_user = User(email=email, password=hashed_password)
            db.add(new_user)
            await db.commit()

        await flash("Account created successfully. Please log in.", "success")
        return redirect(url_for('auth.login'))

    return await render_template('auth/signup.html')


@auth_bp.route('/logout')
@login_required
async def logout():
    from quart_auth import logout_user
    logout_user()
    await flash("You have been logged out.", "success")
    return redirect(url_for('auth.login'))
