$(function() {

    // header/nav menu for mobile devices
    var $headerMenuButton = $('#header-menu-button');
    var $nav = $('nav');

    $headerMenuButton.click(function() {
        $headerMenuButton.toggleClass('active');
        $nav.toggleClass('active');
    })

});
