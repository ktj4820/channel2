// Generated by CoffeeScript 1.6.3
(function() {
  $(function() {
    var $navbar, LabelModelView, markdown;
    $navbar = $('nav');
    $('#header-menu-icon').click(function() {
      return $navbar.toggleClass('active');
    });
    $('.message .icon-cancel').click(function() {
      return $(this).parent().slideUp(200);
    });
    if ($('#template-label-edit').length) {
      markdown = new Markdown.Converter();
      LabelModelView = function() {
        var self;
        self = this;
        self.markdown = ko.observable($('#id_markdown').val());
        self.html = ko.computed(function() {
          return markdown.makeHtml(self.markdown());
        });
        return false;
      };
      return ko.applyBindings(new LabelModelView());
    }
  });

}).call(this);
