#! /usr/bin/python
# -*- coding:utf-8 -*-
from flask import *
import datetime
from decimal import *
from connexion_db import get_db

fixtures_load = Blueprint('fixtures_load', __name__,
                          template_folder='templates')


@fixtures_load.route('/base/init')
def fct_fixtures_load():
    requests = "".join(open("sae_sql.sql").readlines())
    mycursor = get_db().cursor()
    
    for i,sql in enumerate(requests[:-1].split(";")):
        mycursor.execute(sql)

    get_db().commit()
    return redirect('/')
