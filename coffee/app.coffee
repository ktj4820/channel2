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