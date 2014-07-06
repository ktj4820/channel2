$ ->

    #---------------------------------------------------------------------------
    # mobile menu
    #---------------------------------------------------------------------------

    $('#nav-mobile-menu-icon').click ->
        $('nav').toggleClass('active')

    #---------------------------------------------------------------------------
    # back to top
    #---------------------------------------------------------------------------

    $('.back-to-top').click ->
        $('html, body').animate { 'scrollTop': 0 }, 'slow'
        return false

    #---------------------------------------------------------------------------
    # markdown preview
    #---------------------------------------------------------------------------

    markdown = new Markdown.Converter()

    $('.markdown-preview').each ->
        preview = $(this)
        input = $('#' + preview.attr('data-for'))
        input.on 'keyup', -> preview.html(markdown.makeHtml(input.val()))
        preview.html(markdown.makeHtml(input.val()))

        # tags autocomplete
        split = (val) -> val.split(/,\s*/)
        extractLast = (term) -> split(term).pop()

    #---------------------------------------------------------------------------
    # tag autocomplete
    #---------------------------------------------------------------------------

    if ('#template-tag-edit').length

        split = (val) -> val.split(/,\s*/)
        extractLast = (term) -> split(term).pop()

        bindAutocompleteKeydown = (e) ->
            if e.keyCode == $.ui.keyCode.TAB && $(this).data('ui-autocomplete').menu.active
                e.preventDefault()

        autocompleteParams = (source) ->
            return {
                source: (request, response) ->
                    results = $.ui.autocomplete.filter(source, extractLast(request.term))
                    response(results.slice(0, 10))
                delay: 0
                focus: -> return false
                select: (e, ui) ->
                    terms = split(this.value)
                    terms.pop()
                    terms.push(ui.item.value)
                    terms.push('')
                    this.value = terms.join(', ')
                    return false
            }

        success = (data) -> $('#id_children').bind('keydown', bindAutocompleteKeydown).autocomplete(autocompleteParams(data))
        $.get '/tag/autocomplete.json', success

    #---------------------------------------------------------------------------
    # messages
    #---------------------------------------------------------------------------

    $('.message .icon-cancel').click ->
        self = $(this).parent()
        self.slideUp 200, ->
            self.remove()
            messageList = self.parent().parent()
            if not messageList.length
                messageList.remove()

    return
