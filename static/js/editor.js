var canvas;
var blocks = [];
var blockSize = 100;

var trigger_types = {
    rss: {
        inputs: [
            'url'
        ],
        outputs: [
            'url', 'title', 'text', 'time'
        ]
    },
    time: {
        inputs: [
            'time'
        ],
        outputs: [
            'time'
        ]
    }
};

var event_types = {
    text: {
        inputs: [
            'phone', 'message'
        ],
        outputs: [
        ]
    }
};

var conditional_types = {
    'if': {
        inputs: [
            'invalue', 'operation', 'outvalue'
        ],
        outputs: [
            'boolean'
        ]
    }
};

var colors = {
    "conditional": { // orange
        fg: "#FF9800",
        bg: "#F57C00"
    },
    "trigger": { // red
        fg: "#F44336",
        bg: "#D32F2F"
    },
    "event": { // blue
        fg: "#2196F3",
        bg: "#1976D2"
    },
    "none": { // green
        fg: "#4CAF50",
        bg: "#388E3C"
    }
};

function genOptionString(block, gen_type, type) {
    var type_var = null;
    switch(gen_type) {
        case 'conditional':
            type_var = conditional_types;
            break;
        case 'trigger':
            type_var = trigger_types;
            break;
        case 'event':
            type_var = event_types;
            break;
    }
    if(!type_var) {
        return "<option value='null'>Bad genOptionString arguments</option>"
    }
    var ret = "";
    type_var[type].outputs.forEach(function(output) {
        ret += "<option value='"+output+"'>"+output+"</option>";
    });
    return ret;
}

function openInformation(block) {
    var $bod = $("#conditional-modal .modal-body");
    $bod.html("");
    console.log(block.connections);
    if(block.automate_general_type == "trigger"){
        inner_html = "";
        trigger_types[block.automate_type].inputs.forEach(function(input){
            curr_val = "";
            if(block.inputs[input]) curr_val = block.inputs[input];
            inner_html += '<div class="form-group"><div class="input-group"><input id="id_' + input + '" name="' + input + '" type="text" class="form-control" placeholder="' + input + '" value="' + curr_val + '" /></div></div>'
            $(".save-modal").data("id", block.id)
        });
        $("#conditional-modal .modal-body").html(inner_html);
    } else if(block.automate_general_type == "event"){
        inner_html = "";
        event_types[block.automate_type].inputs.forEach(function(input){
            curr_val = "";
            if(block.inputs[input]) curr_val = block.inputs[input];
            inner_html += '<div class="form-group"><div class="input-group"><input id="id_' + input + '" name="' + input + '" type="text" class="form-control" placeholder="' + input + '" value="' + curr_val + '" /></div></div>'
            $(".save-modal").data("id", block.id)
        });
        $("#conditional-modal .modal-body").html(inner_html);
    } else if(block.automate_general_type == "conditional") {
        block.connectionsFrom.forEach(function(from) {
            $bod.append("<div class='option'><p>" + from.name + "</p><select>" +
                genOptionString(from, from.automate_general_type, from.automate_type) + "</select>"
            );
        });
    }
    $("#conditional-modal").modal();
    $("#conditional-modal #save").click(function() {
        // Serialize and send
        $("#conditional-modal").modal('hide');
    });
    $(".save-modal").click(function(){
        block = blocks[$(this).data("id")];
        if(block.automate_general_type == "trigger"){
            trigger_types[block.automate_type].inputs.forEach(function(input){
                block.inputs[input] = $("#id_" + input).val();
                console.log(input);
            });
        }
        console.log(block.inputs)
    });
};

function addBlock(name, type) {
    var rect = new fabric.Rect({
        fill: colors[type || "none"].fg,
        width: blockSize,
        height: blockSize
    });
    rect.stroke = colors[type || "none"].bg;
    rect.strokeWidth = 1;
    var text = new fabric.Text(name, {
        left: blockSize / 2,
        top: blockSize / 2,
        fontSize: 16,
        textAlign: "center",
        originX: "center",
        originY: "center",
        fontFamily: "sans-serif"
    });
    var block = new fabric.Group([rect, text], {
        left: $(window).width() / 2 - blockSize / 2 + blocks.length * 6,
        top: $(window).height() / 2 - blockSize / 2 - $("nav").height() + blocks.length * 6,
        lockRotation: true,
        lockScalingX: true,
        lockScalingY: true,
        lockUniScaling: true
    });
    block.type = "block";
    block.automate_general_type = type;
    block.automate_type = name;
    block.id = blocks.length;
    block.name = name;
    block.inputs = {}
    block.connections = [];
    block.connectionsTo = [];
    block.connectionsFrom = [];
    block.mouseDownCoordinates = null;
    block.on('mousedown', function(e) {
        if($("#default.active").length)
            block.mouseDownCoordinates = [e.e.clientX, e.e.clientY];
    });
    block.on('mouseup', function(e) {
        c = block.mouseDownCoordinates;
        if(c == null) {
            return;
        }
        if((e.e.clientX - c[0])**2 + (e.e.clientY - c[1])**2 == 0) {
            openInformation(block);
        }
        block.mouseDownCoordinates = null;
    });
    block.setControlsVisibility({"mtr": false});
    canvas.add(block);
    blocks.push(block);
    return block;
}

function connectBlocks(a, b) {
    if (a == b) {
        return null;
    }
    var flag = false;
    $.each(a.connections, function(k, v) {
        if (v.from == b || v.to == b) {
            flag = true;
            return false;
        }
    });
    if (flag) {
        return null;
    }
    var line = new fabric.Line([0, 0, 1, 1], {
        stroke: "red",
        strokeWidth: 2,
        originX: "left",
        originY: "top"
    });
    line.type = "line";
    var triangle = new fabric.Triangle({
        angle: 0,
        fill: "red",
        top: 0,
        left: 0,
        height: 25,
        width: 25,
        originX: "center",
        originY: "center",
        selectable: false
    });
    line.triangle = triangle;
    line.from = a;
    line.to = b;
    a.connectionsTo.push(b);
    b.connectionsFrom.push(a);
    a.connections.push(line);
    b.connections.push(line);
    recalculateConnection(line);
    canvas.add(line);
    canvas.add(triangle);
    return line;
}

function recalculateConnection(v) {
    var angle = Math.atan2(v.from.top - v.to.top, v.to.left - v.from.left)*180/Math.PI;
    var fPos = "bottom";
    var tPos = "top";
    if (angle >= -45 && angle <= 45) {
        fPos = "right";
        tPos = "left";
    }
    else if (angle > 0 && angle <= 135) {
        fPos = "top";
        tPos = "bottom";
    }
    else if (Math.abs(angle) > 135) {
        fPos = "left";
        tPos = "right";
    }
    v.left = v.from.left + v.from.width / 2;
    v.top = v.from.top + v.from.height / 2;
    v.width = (v.to.left + v.to.width / 2) - v.left;
    v.set("flipX", v.width < 0);
    if (fPos == "left") {
        v.left += blockSize / 2;
    }
    if (fPos == "right") {
        v.left += blockSize / 2;
    }
    if (fPos == "top") {
        v.top -= blockSize / 2;
    }
    if (fPos == "bottom") {
        v.top += blockSize / 2;
    }
    v.triangle.left = v.left + v.width;
    if (tPos == "left") {
        v.triangle.left -= blockSize;
    }
    if (v.width < 0) {
        v.left += v.width;
    }
    v.width = Math.abs(v.width);
    v.height = (v.to.top + v.to.height / 2) - v.top;
    v.set("flipY", v.height < 0);
    if (tPos == "left") {
        v.width -= blockSize;
    }
    if (tPos == "right") {
        v.width -= blockSize;
    }
    if (tPos == "top") {
        v.height -= blockSize / 2;
    }
    if (tPos == "bottom") {
        v.height += blockSize / 2;
    }
    v.triangle.top = v.top + v.height;
    if (v.height < 0) {
        v.top += v.height;
    }
    v.height = Math.abs(v.height);
    v.triangle.angle = 90 - angle;
}

$(document).ready(function() {
    canvas = new fabric.Canvas("editor", { preserveObjectStacking: true });
    canvas.on("object:moving", function(e) {
        if (e.target.type == "block") {
            $.each(e.target.connections, function(k, v) {
                recalculateConnection(v);
            });
        }
    });
    var lastClick = null;
    var prevBlock = null;
    canvas.on("mouse:down", function(e) {
        lastClick = new Date();
    });
    canvas.on("mouse:up", function(e) {
        var time = new Date().getTime() - lastClick.getTime();
        if (time < 100) {
            var obj = canvas.getActiveObject();
            if (obj && obj.type == "block" && $("#arrow.active").length) {
                if (prevBlock) {
                    connectBlocks(prevBlock, obj);
                    prevBlock = null;
                }
                else {
                    prevBlock = obj;
                }
            }
            else if ($("#delete.active").length) {
                deleteSelected();
            }
        }
    });
    canvas.on("object:removed", function(e) {
        if (e.target.type == "block") {
            $.each(e.target.connections, function(k, v) {
                try {
                    canvas.remove(v);
                }
                finally {
                    v.from.connections.splice(v.from.connections.indexOf(v), 1);
                    v.to.connections.splice(v.to.connections.indexOf(v), 1);
                }
            });
            canvas.deactivateAll();
        }
        if (e.target.type == "line") {
            canvas.remove(e.target.triangle);
        }
    });
    $(window).on("resize", function() {
        var width = window.innerWidth;
        var height = window.innerHeight - $("nav").height();
        $("#content").css("width", width + "px").css("height", height + "px");
        canvas.setWidth(width);
        canvas.setHeight(height);
    });
    function deleteSelected() {
        var group = canvas.getActiveGroup();
        if (group) {
            $.each(group._objects, function(k, v) {
                if (v.type == "block") {
                    try {
                        canvas.remove(v);
                        $.each(v.connections, function(kt, vt) {
                            try {
                                canvas.remove(vt);
                            } catch (e) {  }
                        });
                    }
                    catch (e) { }
                    blocks.splice(blocks.indexOf(v), 1);
                }
            });
        }
        else {
            var obj = canvas.getActiveObject();
            canvas.remove(obj);
            if (obj == "block") {
                blocks.splice(blocks.indexOf(obj), 1);
            }
        }
    }
    $(window).on("keydown", function(e) {
        if (e.keyCode == 46) {
            deleteSelected();
        }
    });
    $(window).resize();

    type_div_map = {
        "#triggers": trigger_types,
        "#events": event_types,
        "#conditionals": conditional_types
    };

    Object.keys(type_div_map).forEach(function(key) {
        types = Object.keys(type_div_map[key]);
        types.forEach(function(t) {
            console.log($(key));
            $(key).append("<div class='"+t+"'>"+t+"</div>");
        });
    });

    $("#triggers div").each(function(i,el) {
        el.onclick = function() {
            addBlock(el.innerHTML, "trigger");
        };
    });
    $("#events div").each(function(i,el) {
        el.onclick = function() {
            addBlock(el.innerHTML, "event");
        };
    });
    $("#conditionals div").each(function(i,el) {
        el.onclick = function() {
            addBlock(el.innerHTML, "conditional");
        };
    });
    $(".tool").click(function() {
        $(".tool").removeClass("active");
        $(this).addClass("active");
    });

    $("#picker-close").click(function(el) {
        $("#picker").toggleClass("closed");
    });
});
