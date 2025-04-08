from flask import render_template, redirect, url_for, session

def mesas():
    return render_template("mesas.html")