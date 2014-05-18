$ ->

    #---------------------------------------------------------------------------
    # mobile menu
    #---------------------------------------------------------------------------

    $nav = $('nav')
    $mobileMenuButton = $('#header-mobile-menu-icon')
    $mobileMenuButton.click -> $nav.toggleClass('active')

    #---------------------------------------------------------------------------
    # back to top
    #---------------------------------------------------------------------------

    $('.back-to-top').click ->
        $('html, body').animate { 'scrollTop': 0 }, 'slow'
        return false

    #---------------------------------------------------------------------------
    # markdown preview
    #---------------------------------------------------------------------------

    $('.markdown-preview').each ->
        preview = $(this)
        input = $('#' + preview.attr('data-for'))
        input.on 'keyup', -> preview.html(markdown.toHTML(input.val()))
        preview.html(markdown.toHTML(input.val()))
