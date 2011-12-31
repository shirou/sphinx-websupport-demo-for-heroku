$(document).ready(function() {
    var url = document.URL.replace(/#.*/, '');
    var parts = url.split('/');

    var base = 'http://docs.python.org/2.7/';
    base += parts[parts.length-2] + '/' + parts[parts.length-1];
    $('a.headerlink').each(function() {
            var html = '<a href="' + base + $(this).attr('href') +
                       '" title="原文へのリンク"><small>(原文)</small></a>';
            $(this).after(html);
        })
});
