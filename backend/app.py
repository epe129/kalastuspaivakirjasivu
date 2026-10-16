"""Flask admin application for the fishing diary site."""

import os
import re

import bcrypt
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_wtf import CSRFProtect, FlaskForm
from flask_mysqldb import MySQL
from MySQLdb import Error as MySQLError
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired, Length

import dbinfo

app = Flask(__name__)
secret_key = os.environ.get("FLASK_SECRET_KEY", "")
if len(secret_key) < 32:
    raise RuntimeError("FLASK_SECRET_KEY must contain at least 32 characters.")
upload_directory = os.environ.get("APP_UPLOAD_DIR")
if not upload_directory:
    raise RuntimeError("APP_UPLOAD_DIR must point to the private image directory.")
if not os.path.isabs(upload_directory):
    raise RuntimeError("APP_UPLOAD_DIR must be an absolute path.")
trusted_hosts = [
    host.strip()
    for host in os.environ.get("FLASK_TRUSTED_HOSTS", "").split(",")
    if host.strip()
]
if not trusted_hosts:
    raise RuntimeError("FLASK_TRUSTED_HOSTS must list the admin site's hostnames.")

app.config.update(
    SECRET_KEY=secret_key,
    TRUSTED_HOSTS=trusted_hosts,
    UPLOAD_DIR=upload_directory,
    MYSQL_HOST=dbinfo.data["HOST"],
    MYSQL_PORT=dbinfo.data["PORT"],
    MYSQL_USER=dbinfo.data["USER"],
    MYSQL_PASSWORD=dbinfo.data["PASSWORD"],
    MYSQL_DB=dbinfo.data["DBNIMI"],
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SECURE=os.environ.get("COOKIE_SECURE", "1") == "1",
    SESSION_COOKIE_SAMESITE="Lax",
    PERMANENT_SESSION_LIFETIME=60 * 60,
    MAX_CONTENT_LENGTH=16 * 1024,
)

mysql = MySQL(app)
CSRFProtect(app)


class MyForm(FlaskForm):
    """Administrator login form."""

    username = StringField(
        "Username", validators=[InputRequired(), Length(max=45)]
    )
    password = PasswordField(
        "Password", validators=[InputRequired(), Length(max=72)]
    )


def admin_required():
    admin_id = session.get("id")
    if not session.get("logged_in") or not isinstance(admin_id, int):
        session.clear()
        return redirect(url_for("login"))
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT username FROM admin WHERE id = %s", (admin_id,))
    admin = cursor.fetchone()
    if not admin or admin[0] != session.get("username"):
        session.clear()
        return redirect(url_for("login"))
    return None


def selected_id(field):
    try:
        value = int(request.form.get(field, ""))
    except (TypeError, ValueError):
        return None
    return value if value > 0 else None


@app.after_request
def add_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; img-src 'self'; style-src 'self' 'unsafe-inline'; "
        "script-src 'self'; object-src 'none'; base-uri 'self'; "
        "frame-ancestors 'none'; form-action 'self'"
    )
    if app.config["SESSION_COOKIE_SECURE"]:
        response.headers["Strict-Transport-Security"] = (
            "max-age=31536000"
        )
    return response


@app.route("/", methods=["GET", "POST"])
def login():
    """Authenticate an administrator and display the login page."""
    form = MyForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        cursor = mysql.connection.cursor()
        cursor.execute(
            "SELECT id, username, pword FROM admin WHERE username = %s",
            (username,),
        )
        user = cursor.fetchone()
        if user:
            stored_hash = user[2]
            if isinstance(stored_hash, str):
                stored_hash = stored_hash.encode("utf-8")
            try:
                password_bytes = form.password.data.encode("utf-8")
                password_matches = len(password_bytes) <= 72 and bcrypt.checkpw(
                    password_bytes, stored_hash
                )
            except ValueError:
                password_matches = False
            if password_matches:
                session.clear()
                session.permanent = True
                session["id"] = user[0]
                session["username"] = user[1]
                session["logged_in"] = True
                return redirect(url_for("home"))
        flash("Invalid username or password.", "error")
        form.password.data = ""
    return render_template("login.html", form=form)


@app.route("/home")
def home():
    """Show database record counts to an authenticated administrator."""
    denied = admin_required()
    if denied:
        return denied

    cursor = mysql.connection.cursor()
    counts = {}
    for key, table in (
        ("users_count", "kalastaja"),
        ("species_count", "laji"),
        ("rods_count", "vapa"),
        ("lures_count", "viehe"),
    ):
        cursor.execute(f"SELECT COUNT(*) FROM {table}")
        counts[key] = cursor.fetchone()[0]
    return render_template("home.html", **counts)


@app.route("/poista")
def poista():
    """List records available for administrator deletion."""
    denied = admin_required()
    if denied:
        return denied

    cursor = mysql.connection.cursor()
    cursor.execute("SELECT id, email FROM kalastaja ORDER BY id")
    users = cursor.fetchall()
    cursor.execute("SELECT id, laji FROM laji ORDER BY id")
    species = cursor.fetchall()
    cursor.execute("SELECT id, vapa FROM vapa ORDER BY id")
    rods = cursor.fetchall()
    cursor.execute("SELECT id, viehe FROM viehe ORDER BY id")
    lures = cursor.fetchall()
    return render_template(
        "poista.html", users=users, laji=species, vapa=rods, viehe=lures
    )


@app.post("/delete_user")
def delete_user():
    """Delete an angler and their catch records in a single transaction."""
    denied = admin_required()
    if denied:
        return denied
    user_id = selected_id("users")
    if user_id is None:
        flash("Select a valid angler.", "error")
        return redirect(url_for("poista"))

    cursor = mysql.connection.cursor()
    cursor.execute(
        "SELECT kala.kuva FROM kala "
        "JOIN tarppi ON tarppi.id = kala.tarppi_id "
        "WHERE tarppi.kalastaja_id = %s AND kala.kuva IS NOT NULL",
        (user_id,),
    )
    image_names = [row[0] for row in cursor.fetchall()]
    try:
        cursor.execute("START TRANSACTION")
        cursor.execute(
            "DELETE kala FROM kala "
            "JOIN tarppi ON tarppi.id = kala.tarppi_id "
            "WHERE tarppi.kalastaja_id = %s",
            (user_id,),
        )
        cursor.execute("DELETE FROM tarppi WHERE kalastaja_id = %s", (user_id,))
        cursor.execute("DELETE FROM kalastaja WHERE id = %s", (user_id,))
        if cursor.rowcount == 0:
            mysql.connection.rollback()
            flash("Angler was not found.", "error")
        else:
            mysql.connection.commit()
            cleanup_failed = False
            for name in image_names:
                if re.fullmatch(r"[a-f0-9]{32}\.(?:jpg|png|gif)", name):
                    path = os.path.join(app.config["UPLOAD_DIR"], name)
                    if os.path.isfile(path):
                        try:
                            os.remove(path)
                        except OSError:
                            app.logger.exception("Failed to remove an angler's private image.")
                            cleanup_failed = True
            if cleanup_failed:
                flash(
                    "Angler and catches were deleted, but one or more private images could not be removed.",
                    "error",
                )
            else:
                flash("Angler and their catch records were deleted.", "success")
    except MySQLError:
        mysql.connection.rollback()
        raise
    return redirect(url_for("poista"))


def delete_unused_reference(table, reference_table, reference_column, field):
    """Delete a lookup value only when no saved catch references it."""
    denied = admin_required()
    if denied:
        return denied
    item_id = selected_id(field)
    if item_id is None:
        flash("Select a valid item.", "error")
        return redirect(url_for("poista"))

    cursor = mysql.connection.cursor()
    cursor.execute(
        f"SELECT COUNT(*) FROM {reference_table} WHERE {reference_column} = %s",
        (item_id,),
    )
    if cursor.fetchone()[0]:
        flash("This item is in use and cannot be deleted.", "error")
    else:
        cursor.execute(f"DELETE FROM {table} WHERE id = %s", (item_id,))
        mysql.connection.commit()
        flash("Item deleted.", "success")
    return redirect(url_for("poista"))


@app.post("/delete_vapa")
def delete_vapa():
    """Delete a rod that is not referenced by any catch."""
    return delete_unused_reference("vapa", "tarppi", "vapa_id", "vapa")


@app.post("/delete_laji")
def delete_laji():
    """Delete a species that is not referenced by any fish record."""
    return delete_unused_reference("laji", "kala", "laji_id", "laji")


@app.post("/delete_viehe")
def delete_viehe():
    """Delete a lure that is not referenced by any catch."""
    return delete_unused_reference("viehe", "tarppi", "viehe_id", "viehe")


@app.post("/logout")
def logout():
    """Clear the administrator session."""
    session.clear()
    return redirect(url_for("login"))


if __name__ == "__main__":
    app.run(debug=False, use_reloader=False)
