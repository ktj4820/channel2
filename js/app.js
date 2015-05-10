$(function() {

    // header/nav menu for mobile devices
    var $headerMenuButton = $('#header-menu-button');
    var $nav = $('nav');

    $headerMenuButton.click(function() {
        $headerMenuButton.toggleClass('active');
        $nav.toggleClass('active');
    });

    // messages
    $('.message .icon-cancel').click(function () {
        $(this).parent().slideUp(200);
    });

    // markdown preview
    var $mdPreview = $('.markdown-preview');
    if ($mdPreview.length) {
        $mdPreview.each(function() {
            var preview = $(this);
            var input = $('#' + preview.attr('data-for'));
            input.on('keyup', function() {
                preview.html(markdown.toHTML(input.val()));
            });
            preview.html(markdown.toHTML(input.val()));
        });
    }

    // tag autocomplete
    if (('#template-staff-tag').length) {
        var split = function(val) { return val.split(/,\s*/); };
        var extractLast = function(term) { return split(term).pop(); };

        var bindAutocompleteKeydown = function(e) {
            if (e.keyCode == $.ui.keyCode.TAB && $(this).data('ui-autocomplete').menu.active) {
                e.preventDefault();
            }
        };

        var autocompleteParams = function(source) {
            return {
                source: function(request, response) {
                    var results = $.ui.autocomplete.filter(source, extractLast(request.term));
                    return response(results.slice(0, 10));
                },
                delay: 0,
                focus: function() { return false; },
                select: function(e, ui) {
                    var terms = split(this.value);
                    terms.pop();
                    terms.push(ui.item.value);
                    terms.push('');
                    this.value = terms.join(', ');
                    return false
                }
            }
        };

        $.get('/staff/tag/autocomplete.json', function(data) {
            $('#id_children').bind('keydown', bindAutocompleteKeydown).autocomplete(autocompleteParams(data));
        });
    }

});
