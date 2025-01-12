(function($) {
    'use strict';
    
    window.formatIconOption = function(option) {
        if (!option.id) return option.text;
        return '<div class="icon-option">' +
               '<i class="' + option.id + ' fa-fw"></i> ' +
               '<span class="icon-text">' + option.text + '</span>' +
               '</div>';
    }

    function initIconSelect() {
        $('.icon-select').select2({
            templateResult: formatIconOption,
            templateSelection: formatIconOption,
            escapeMarkup: function(m) { return m; }
        });
    }

    // Handle both admin and frontend contexts
    if (typeof django !== 'undefined' && django.jQuery) {
        django.jQuery(document).ready(function() {
            initIconSelect();
        });
    } else if (typeof $ !== 'undefined') {
        $(document).ready(function() {
            initIconSelect();
        });
    }
})(window.django ? django.jQuery : jQuery); 