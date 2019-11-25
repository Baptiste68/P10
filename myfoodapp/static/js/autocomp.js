$(function() {
    $('.autocomp').autocomplete({
        source: "/myfoodapp/autocomplete/",
        minLength: 3,
    });
});