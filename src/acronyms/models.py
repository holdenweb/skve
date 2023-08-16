"""
models.py

Interactions for the acronyms app.
"""

import mongoengine as me

class Acronym(me.Document):
    acronym = me.StringField(required=True)
    title = me.StringField(required=True)
    explanation = me.StringField()
    further_info = me.StringField()
    linked_item = me.StringField()
    text_explanation = me.StringField()



