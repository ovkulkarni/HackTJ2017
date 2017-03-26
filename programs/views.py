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
                },
            'twitter': {
                    "handle": "string"
                },
            'if': {
                    'inner': 'string',
                    'oper': 'string',
                    'outer': 'string'
                }
        }

RESULTS_MAPPINGS = {
            'rss': {
                    "url": "string",
                    "title": "string",
                    "text": "string"
                },
            'twitter': {
                    'handle': 'string',
                    'body': 'string',
                    'date': 'string'
                }
        }

@blueprint.route("/editor/")
@login_required
def editor():
    return render_template("editor.html", user=g.user)

@blueprint.route("/editor/<int:id>/")
@login_required
def edit(id):
    return render_template("editor.html", user=g.user, prog_id=id)

@blueprint.route("/delete/<int:id>")
@login_required
def delete(id):
    p = Program.get(Programs.id == id)
    if(g.user == p.owner):
        p.delete()
    return render_template("index.html", user=g.user)


@blueprint.route("/save/", methods=["POST"])
@login_required
def save():
    prgrm = json.loads(request.form.get("program"))
    print(prgrm)
    p = Program.create(owner=g.user)
    process_program(prgrm, p)
    return jsonify({"success": True})

def process_program(prgrm, p):
    db_blocks = []
    for block in prgrm:
        if block["type"] == "trigger":
            t = Trigger.create(trigger_type=block["name"], args=formatted_args(block), results=formatted_results(block))
            b = Block.create(program=p, block_type="t", trigger=t)
            db_blocks.append(b)
        elif block["type"] == "event":
            e = Event.create(args=formatted_args(block, db_blocks), action=block["name"])
            b = Block.create(program=p, block_type="e", event=e)
            db_blocks.append(b)
        elif block["type"] == "conditional":
            in_args = process_value(block["values"]["left"], db_blocks)
            check = block["values"]["operator"]
            out_args = process_value(block["values"]["right"], db_blocks)
            c = Condition.create(in_val=in_args, check=check, out_val=out_args)
            b = Block.create(program=p, block_type="c", condition=c)
            inner_b = process_program(block["inner"], p)
            outer_b = process_program(block["outer"], p)
            cl = ConditionalLink.create(condition=c, inner=inner_b, outer=outer_b)
            db_blocks.append(b)
    for i, val in enumerate(db_blocks[:-1]):
        l = Link.create(source=db_blocks[i], destination=db_blocks[i+1])
    return db_blocks[0]

def process_value(val, all_blocks=[]):
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
    return val

def formatted_args(block, all_blocks=[]):
    args = "["
    for key in ARGS_MAPPINGS[block["name"]]:
        args += "('{}', '{}', '{}'), ".format(process_value(block["values"][key], all_blocks), key, ARGS_MAPPINGS[block["name"]][key])
    args = args[:-2]
    args += "]"
    return args

def formatted_results(block):
    results = "["
    for key in RESULTS_MAPPINGS[block["name"]]:
        results += "('{}', '{}'), ".format(key, RESULTS_MAPPINGS[block["name"]][key])
    results = results[:-2]
    results += "]"
    return results
