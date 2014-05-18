$ ->

    #---------------------------------------------------------------------------
    # mobile menu
    #---------------------------------------------------------------------------

    $nav = $('nav')
    $mobileMenuButton = $('#header-mobile-menu-icon')
    $mobileMenuButton.click -> $nav.toggleClass('active')
