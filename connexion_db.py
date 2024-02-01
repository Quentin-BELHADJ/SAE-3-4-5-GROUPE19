from flask import Flask, request, render_template, redirect, url_for, abort, flash, session, g
import pymysql.cursors
import os                                 # à ajouter
from dotenv import load_dotenv            # à ajouter
load_dotenv()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        #
        db = g._database = pymysql.connect(
            host="localhost",
            user="audrick",
            password="mdp",
            database="S2",
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    return db