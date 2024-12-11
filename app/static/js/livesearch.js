function setupLiveSearch(tableId, searchInputId, filterSelectId, options) {
	const searchInput = document.getElementById(searchInputId);
	const filterSelect = document.getElementById(filterSelectId);
	const table = document.getElementById(tableId);
	const rows = table
		.getElementsByTagName("tbody")[0]
		.getElementsByTagName("tr");

	options.forEach((option) => {
		const optElement = document.createElement("option");
		optElement.value = option.value;
		optElement.textContent = option.label;
		filterSelect.appendChild(optElement);
	});

	function performSearch() {
		const searchTerm = searchInput.value.toLowerCase();
		const selectedFilter = filterSelect.value;

		for (let row of rows) {
			let cells = Array.from(row.getElementsByTagName("td"));
			let searchableText = "";

			switch (selectedFilter) {
				case "id":
					searchableText = cells[0].textContent.toLowerCase();
					break;
				case "name":
					searchableText = cells[1].textContent.toLowerCase();
					break;
				case "code":
					searchableText = cells[1].textContent.toLowerCase();
					break;
				case "courseName":
					searchableText = cells[2].textContent.toLowerCase();
					break;
				default:
					searchableText = cells
						.slice(0, -1)
						.map((cell) => cell.textContent.toLowerCase())
						.join(" ");
			}

			const foundMatch = searchableText.includes(searchTerm);
			row.style.display = foundMatch ? "" : "none";
		}
	}

	searchInput.addEventListener("keyup", performSearch);
	filterSelect.addEventListener("change", performSearch);
}
