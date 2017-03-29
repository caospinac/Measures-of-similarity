$(function(argument) {
    $('#addItem').click(function(e) {

        var btn = $('<a></a>');
        btn.attr('class', 'delete');
        btn.append('Delete');
        btn.click(function(e) {
            $(this).parent().remove();
        });

        var fieldName = $('<input></input>');
        fieldName.attr({
            class: 'fieldName',
            type: 'text',
            name: 'names',
            placeholder: 'Field name',
            autocomplete: 'off',
            required: 'true'
        });
        fieldName.keypress(function(e) {
            if (e.which == 13) {
                $(this).next().focus();
                return false;
            }
        });

        var textArea = $('<textarea></textarea>');
        textArea.attr({
            name: 'values',
            placeholder: 'Content'
        });

        var newItem = $('<div></div>');
        newItem.attr('class', 'item');
        newItem.append(btn);
        newItem.append(fieldName);
        newItem.append(textArea);

        $("#items").append(newItem);
    });

    

    // $('#addItem').click();
});