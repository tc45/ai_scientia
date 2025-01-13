(function($) {
    'use strict';
    
    // Initialize when dependencies are ready
    function initSelect2() {
        if (typeof $.fn.select2 === 'undefined') {
            setTimeout(initSelect2, 100);
            return;
        }

        function formatOption(option) {
            if (!option.id) return option.text;
            
            var iconClass = $(option.element).data('icon');
            if (!iconClass) return option.text;
            
            return $('<span>')
                .append($('<i>').addClass(iconClass))
                .append(' ' + option.text);
        }

        $('.icon-select').each(function() {
            $(this).select2({
                templateResult: formatOption,
                templateSelection: formatOption,
                escapeMarkup: function(m) { return m; }
            });
        });
    }

    // Start initialization
    if (typeof jQuery !== 'undefined') {
        $(document).ready(initSelect2);
    } else {
        document.addEventListener('DOMContentLoaded', function() {
            if (typeof jQuery !== 'undefined') {
                initSelect2();
            }
        });
    }
})(django.jQuery || jQuery);