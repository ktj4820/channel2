$ ->

    #---------------------------------------------------------------------------
    # nav menu
    #---------------------------------------------------------------------------

    $navbar = $('nav')
    $('#header-menu-icon').click -> $navbar.toggleClass('active')

    #---------------------------------------------------------------------------
    # messages
    #---------------------------------------------------------------------------

    $('.message .icon-cancel').click -> $(this).parent().slideUp(200)

    #---------------------------------------------------------------------------
    # label markdown editor
    #---------------------------------------------------------------------------

    if $('#template-label-edit').length

        markdown = new Markdown.Converter()

        LabelModelView = ->
            self = this

            self.markdown   = ko.observable $('#id_markdown').val()
            self.html       = ko.computed -> return markdown.makeHtml(self.markdown())

            return false

        ko.applyBindings(new LabelModelView())
