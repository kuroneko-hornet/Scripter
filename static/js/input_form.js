var text_str;
var font_size;
var p_index = 0;


const make_input = (element_tag, idname, type, defalut_val) => {
    const input_object = document.createElement(element_tag);
    id_and_name = idname + String(p_index);
    input_object.type = type;
    input_object.defaultValue = default_val;
    input_object.id = id_and_name;
    input_object.name = id_and_name;
    input_object.required;
    return input_object
}


const add_input_to_paragraph = (paragraph, input_title, input_idname, input_type, default_val) => {
    const input_object = make_input(element_tag="input", idname=input_idname, type=input_type, default_val=default_val);
    paragraph.innerHTML += " " + input_title + ": ";
    paragraph.appendChild(input_object);
    return paragraph
}


const add_form = () => {    
    // make paragraph
    var new_paragraph = document.createElement("p");
    new_paragraph.id = "input_p" + String(p_index);
    
    const br = document.createElement("br");

    // make input for text
    add_input_to_paragraph(new_paragraph, input_title="text", input_idname="input_text", input_type="text", default_val="sample_text");
    // make input for font size
    add_input_to_paragraph(new_paragraph, input_title="font size", input_idname="input_fontsize", input_type="number", default_val=64);
    // make input for start
    add_input_to_paragraph(new_paragraph, input_title="start", input_idname="input_start", input_type="number", default_val=0);
    // make input for end
    add_input_to_paragraph(new_paragraph, input_title="end", input_idname="input_end", input_type="number", default_val=5);

    new_paragraph.appendChild(br);
    // make input for color
    add_input_to_paragraph(new_paragraph, input_title="color", input_idname="input_color", input_type="text", default_val="black");
    // make input for xy_mode
    add_input_to_paragraph(new_paragraph, input_title="xy_mode", input_idname="input_xy_mode", input_type="text", default_val="");

    // add paragraph to form
    const send_button = document.getElementById("addform_button");
    send_button.before(new_paragraph)
    p_index++;
}
