document.addEventListener('DOMContentLoaded', function() {
    const filterForm = document.getElementById('filterForm');
    const difficultyAll = document.getElementById('difficultyAll');
    const difficultyFilters = document.querySelectorAll('.filter-difficulty:not(#difficultyAll)');
    const categoryFilters = document.querySelectorAll('.filter-category');
    const searchInput = document.getElementById('tutorialSearch');

    function updateTutorials() {
        // Get selected difficulties (excluding 'all' if specific ones are selected)
        const selectedDifficulties = Array.from(document.querySelectorAll('.filter-difficulty:checked'))
            .map(cb => cb.value)
            .filter(value => value !== 'all' || !Array.from(difficultyFilters).some(cb => cb.checked));

        const selectedCategories = Array.from(categoryFilters)
            .filter(cb => cb.checked)
            .map(cb => cb.value);

        const formData = new FormData();
        selectedDifficulties.forEach(d => formData.append('difficulties[]', d));
        selectedCategories.forEach(c => formData.append('categories[]', c));
        if (searchInput.value) {
            formData.append('search', searchInput.value);
        }

        htmx.ajax('GET', filterForm.getAttribute('hx-get') + '?' + new URLSearchParams(formData), {
            target: '#tutorialList',
            swap: 'innerHTML'
        });
    }

    // Handle difficulty filters
    difficultyAll.addEventListener('change', function() {
        if (this.checked) {
            difficultyFilters.forEach(cb => {
                cb.checked = false;
                cb.disabled = true;
            });
        } else {
            difficultyFilters.forEach(cb => {
                cb.disabled = false;
            });
        }
        updateTutorials();
    });

    difficultyFilters.forEach(cb => {
        cb.addEventListener('change', function() {
            const anyDifficultySelected = Array.from(difficultyFilters).some(cb => cb.checked);
            difficultyAll.checked = !anyDifficultySelected;
            updateTutorials();
        });
    });

    // Handle category filters
    categoryFilters.forEach(cb => {
        cb.addEventListener('change', updateTutorials);
    });

    // Handle search input with debounce
    let searchTimeout;
    searchInput.addEventListener('input', function() {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(updateTutorials, 500);
    });
}); 