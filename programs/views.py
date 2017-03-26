import json

from flask import Blueprint, request, redirect, flash, g, render_template, url_for, session, jsonify

from .models import Program, Trigger, Event, Condition, Loop, Block, Link, ConditionLink

from decorators import login_required

import re

matcher = re.compile(r"^.*{{ (.*) }}.*$")

blueprint = Blueprint("programs", __name__, url_prefix="/program")

ARGS_MAPPINGS = {
            'rss': {
                    "url": "string"
                },
            'sms': {
                    "phone": "string",
                    "message": "string"
                }
        }

RESULTS_MAPPINGS = {
            'rss': {
                    "url": "string",
                    "title": "string",
                    "text": "string"
                }
        }

@blueprint.route("/editor/")
@login_required
def editor():
    return render_template("editor.html", user=g.user)


@blueprint.route("/save/", methods=["POST"])
@login_required
def save():
    prgrm = json.loads(request.form.get("program"))
    p = Program.create(owner=g.user)
    db_blocks = []
    for block in prgrm:
        if block["type"] == "trigger":
            t = Trigger.create(trigger_type=block["name"], args=formatted_args(block), results=formatted_results(block))
            b = Block.create(program=p, block_type="t", trigger=t)
            db_blocks.append(b)
        elif block["type"] == "event":
            e = Event.create(args=formatted_args(block, db_blocks), action=block["name"])
            b = Block.create(program=p, block_type="e", event=e)
            db_blocks.append(e)
    for i, val in enumerate(db_blocks[:-1]):
        l = Link.create(source=val, destination=db_blocks[i+1])
    return jsonify({"success": True})

def formatted_args(block, all_blocks=None):
    args = "["
    for key in ARGS_MAPPINGS[block["name"]]:
        val = block["values"][key]
        match = matcher.match(val)
        if match:
            new_val = match.group(1)
            block_type = new_val.split(".")[0]
            val_block = None
            for b in all_blocks:
                if b.block_type == "t":
                    if b.trigger.trigger_type == block_type:
                        val_block = b
                elif b.block_type == "e":
                    if b.event.action == block_type:
                        val_block = b
            get_val = new_val.split(".")[1]
            val = re.sub("{{.*}}", "{" + "id_{}[{}]".format(val_block.id, get_val)+ "}", val)
        args += "('{}', '{}', '{}')".format(val, key, ARGS_MAPPINGS[block["name"]][key])
    args += "]"
    return args

def formatted_results(block):
    results = "["
    for key in RESULTS_MAPPINGS[block["name"]]:
        results += "('{}', '{}')".format(key, RESULTS_MAPPINGS[block["name"]][key])
    results += "]"
    return results
