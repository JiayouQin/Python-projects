from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from main import db
#-------------add entries
import os
from markupsafe import Markup # this will make html renderable
from os import path
from main import entries,users,utility

try:
    print(utility.query.filter_by(name="Last_entry_id").first().param)
except:
    db.session.add(utility("Last_entry_id",20))

try:
    print(utility.query.filter_by(name="Last_reply_id").first().param)
except:
    db.session.add(utility("Last_reply_id",20))
    
db.session.commit()



#----------------------------