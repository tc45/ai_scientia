document.addEventListener('DOMContentLoaded', function() {
	const filterForm = document.getElementById('filterForm');
	const difficultyAll = document.getElementById('difficultyAll');
	const difficultyFilters = document.querySelectorAll('.filter-difficulty:not(#difficultyAll)');
	const categoryFilters = document.querySelectorAll('.filter-category');
	const searchInput = document.getElementById('demoSearch');
	const clearSearch = document.getElementById('clearSearch');
	const toggleFilters = document.getElementById('toggleFilters');
	const filtersSidebar = document.getElementById('filtersSidebar');
	const useCaseAll = document.getElementById('useCaseAll');
	const useCaseFilters = document.querySelectorAll('.filter-use-case:not(#useCaseAll)');

	function getSubcategories(categoryId) {
		const subcategoriesDiv = document.getElementById(`subcategories${categoryId}`);
		return subcategoriesDiv ? subcategoriesDiv.querySelectorAll('.filter-category') : [];
	}

	function getAllChildCategories(categoryId) {
		const children = [];
		const subcategories = getSubcategories(categoryId);
		subcategories.forEach(sub => {
			children.push(sub);
			const subId = sub.id.replace('subcategory', '').replace('category', '');
			const subChildren = getAllChildCategories(subId);
			children.push(...subChildren);
		});
		return children;
	}

	function updateDemos() {
		const formData = new FormData();
		let hasFilters = false;
		
		// Add search if present
		if (searchInput && searchInput.value.trim()) {
			formData.append('search', searchInput.value.trim());
			hasFilters = true;
		}

		// Handle difficulties - only add if specific difficulties are selected
		const selectedDifficulties = Array.from(difficultyFilters)
			.filter(cb => cb.checked)
			.map(cb => cb.value);
		if (selectedDifficulties.length > 0) {
			selectedDifficulties.forEach(value => formData.append('difficulties[]', value));
			hasFilters = true;
		}

		// Handle use cases - only add if specific use cases are selected
		const selectedUseCases = Array.from(useCaseFilters)
			.filter(cb => cb.checked)
			.map(cb => cb.value);
		if (selectedUseCases.length > 0) {
			selectedUseCases.forEach(value => formData.append('use_cases[]', value));
			hasFilters = true;
		}

		// Update category handling with debugging
		const checkedCategories = Array.from(categoryFilters)
			.filter(cb => cb.checked);

		console.log('Checked categories:', checkedCategories);
		checkedCategories.forEach(cb => {
			console.log('Checkbox details:', {
				id: cb.id,
				value: cb.getAttribute('value'),
				isParent: cb.id.startsWith('category'),
				checked: cb.checked
			});
		});

		// Get all checked categories that have values
		const selectedCategories = checkedCategories
			.filter(cb => {
				const value = cb.getAttribute('value') || cb.value;
				if (!value || !value.trim()) return false;

				// If this is a parent category
				if (cb.id.startsWith('category')) {
					// Include parent only if it's explicitly checked
					return cb.checked;
				} else {
					// For subcategories, include only if parent isn't checked
					const categoryId = cb.id.replace('subcategory', '');
					const parentDiv = cb.closest('.collapse');
					if (parentDiv) {
						const parentId = parentDiv.id.replace('subcategories', '');
						const parentCheckbox = document.getElementById(`category${parentId}`);
						return !parentCheckbox || !parentCheckbox.checked;
					}
					return true;
				}
			})
			.map(cb => {
				const value = cb.getAttribute('value') || cb.value;
				console.log('Final category value:', value);
				return value;
			})
			.filter(value => value && value.trim());

		console.log('Selected categories:', selectedCategories);

		if (selectedCategories.length > 0) {
			selectedCategories.forEach(value => {
				formData.append('categories[]', value);
				hasFilters = true;
			});
		}

		// Log the final form data
		console.log('Has filters:', hasFilters);
		console.log('Form data:', Array.from(formData.entries()));

		// Determine the URL based on whether we have any filters
		const baseUrl = filterForm.getAttribute('hx-get');
		const url = hasFilters ? 
			baseUrl + '?' + new URLSearchParams(formData) : 
			baseUrl;

		console.log('Final URL:', url);

		// Perform AJAX request
		htmx.ajax('GET', url, {
			target: '#demoList',
			swap: 'innerHTML'
		});
	}

	// Handle difficulty filters
	if (difficultyAll) {
		difficultyAll.addEventListener('change', function() {
			difficultyFilters.forEach(cb => {
				if (this.checked) {
					cb.checked = false;
				}
			});
			updateDemos();
		});
	}

	difficultyFilters.forEach(cb => {
		cb.addEventListener('change', function() {
			const anyDifficultySelected = Array.from(difficultyFilters).some(cb => cb.checked);
			if (difficultyAll) {
				difficultyAll.checked = !anyDifficultySelected;
				if (!anyDifficultySelected) {
					difficultyAll.checked = true;
				}
			}
			updateDemos();
		});
	});

	// Handle category filters
	categoryFilters.forEach(cb => {
		cb.addEventListener('change', function() {
			// Handle parent-child relationship
			const categoryId = this.id.replace('subcategory', '').replace('category', '');
			const allChildren = getAllChildCategories(categoryId);
			
			// Set all children to match parent's state
			allChildren.forEach(child => {
				child.checked = this.checked;
			});

			// If this is a child category, check if we need to update parent
			const parentDiv = this.closest('.collapse');
			if (parentDiv) {
				const parentId = parentDiv.id.replace('subcategories', '');
				const parentCheckbox = document.getElementById(`category${parentId}`);
				if (parentCheckbox) {
					const siblings = Array.from(getSubcategories(parentId));
					const allSiblingsChecked = siblings.every(sib => sib.checked);
					parentCheckbox.checked = allSiblingsChecked;
					
					// Also check grandparent if needed
					const grandparentDiv = parentCheckbox.closest('.collapse');
					if (grandparentDiv) {
						const grandparentId = grandparentDiv.id.replace('subcategories', '');
						const grandparentCheckbox = document.getElementById(`category${grandparentId}`);
						if (grandparentCheckbox) {
							const uncles = Array.from(getSubcategories(grandparentId));
							grandparentCheckbox.checked = uncles.every(uncle => uncle.checked);
						}
					}
				}
			}

			updateDemos();
		});
	});

	// Handle use case filters
	if (useCaseAll) {
		useCaseAll.addEventListener('change', function() {
			useCaseFilters.forEach(cb => {
				if (this.checked) {
					cb.checked = false;
				}
			});
			updateDemos();
		});
	}

	useCaseFilters.forEach(cb => {
		cb.addEventListener('change', function() {
			const anyUseCaseSelected = Array.from(useCaseFilters).some(cb => cb.checked);
			if (useCaseAll) {
				useCaseAll.checked = !anyUseCaseSelected;
				if (!anyUseCaseSelected) {
					useCaseAll.checked = true;
				}
			}
			updateDemos();
		});
	});

	// Handle search input with debounce
	if (searchInput) {
		let searchTimeout;
		searchInput.addEventListener('input', function() {
			clearTimeout(searchTimeout);
			searchTimeout = setTimeout(updateDemos, 500);
		});
	}

	// Clear search functionality
	if (clearSearch) {
		clearSearch.addEventListener('click', function(e) {
			e.preventDefault();
			searchInput.value = '';
			updateDemos();
		});
	}

	// Toggle filters for mobile view
	if (toggleFilters && filtersSidebar) {
		toggleFilters.addEventListener('click', function() {
			filtersSidebar.classList.toggle('d-none');
		});
	}
}); 