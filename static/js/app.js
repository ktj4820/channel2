$(function() {

    // toggle menu for mobile devices
    var $headerMobileMenuIcon = $('#header-mobile-menu-icon');
    var $nav = $('nav');
    $headerMobileMenuIcon.click(function() { $nav.toggleClass('active'); })

});
