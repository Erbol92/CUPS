function initializeTooltips() {
    $('[data-toggle="tooltip"]').tooltip({
        delay: { "show": 50, "hide": 100 }
    });
}

$(document).ready(function() {
    initializeTooltips();
});