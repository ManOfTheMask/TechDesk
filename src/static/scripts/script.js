var selectAllCheckbox = document.getElementById('select-all');
    var selectItemCheckboxes = document.getElementsByName('ticket_id');

    selectAllCheckbox.addEventListener('change', function() {
        for (var i = 0; i < selectItemCheckboxes.length; i++) {
            selectItemCheckboxes[i].checked = selectAllCheckbox.checked;
        }
    });