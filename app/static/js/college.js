document
	.getElementById("submitAddCollege")
	.addEventListener("click", function () {
		const collegeName = document.getElementById("name").value;
		const abbreviation = document.getElementById("abbreviation").value;
		const errorDiv = document.querySelector(".error");
		const csrfToken = document.querySelector(
			'#addCollegeForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");
		errorDiv.innerText = "";

		if (collegeName === "") {
			errorDiv.innerText = "College Name is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch("/add_college", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				abbreviation: abbreviation,
				name: collegeName,
			}),
		})
			.then((response) => {
				if (!response.ok) {
					return response.json().then((errorData) => {
						throw errorData;
					});
				}
				return response.json();
			})
			.then((result) => {
				alert(result.message);
				location.reload();
			})
			.catch((error) => {
				errorDiv.innerText =
					error.message || "An error occurred. Please try again.";
				errorDiv.classList.remove("d-none");
				console.error("Error:", error);
			});
	});

document.querySelectorAll(".btn-edit").forEach((button) => {
	button.addEventListener("click", function () {
		const row = this.closest("tr");
		const collegeAbbreviation = this.dataset.id;
		const abbreviation = row.cells[0].textContent;
		const name = row.cells[1].textContent;

		document.getElementById("editCollegeId").value = collegeAbbreviation;
		document.getElementById("editCollegeAbbreviation").value = abbreviation;
		document.getElementById("editCollegeName").value = name;

		new bootstrap.Modal(document.getElementById("editCollegeModal")).show();
	});
});

document
	.getElementById("submitEditCollege")
	.addEventListener("click", function () {
		const collegeAbbreviation = document.getElementById("editCollegeId").value;
		const abbreviation = document.getElementById(
			"editCollegeAbbreviation"
		).value;
		const name = document.getElementById("editCollegeName").value;
		const errorDiv = document.querySelector("#editCollegeModal .error");
		const csrfToken = document.querySelector(
			'#editCollegeForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");

		if (!name) {
			errorDiv.innerText = "Please fill out all fields.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch(`/update_college/${collegeAbbreviation}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				abbreviation: abbreviation,
				name: name,
			}),
		})
			.then((response) => response.json())
			.then((result) => {
				if (result.success) {
					alert(result.message);
					location.reload();
				} else {
					throw new Error(result.message);
				}
			})
			.catch((error) => {
				errorDiv.innerText = error.message;
				errorDiv.classList.remove("d-none");
			});
	});

document.querySelectorAll(".btn-delete").forEach((button) => {
	button.addEventListener("click", function () {
		const collegeAbbreviation = this.dataset.id;
		const csrfToken = document.querySelector(
			'#addCollegeForm input[name="csrf_token"]'
		).value;

		if (confirm("Are you sure you want to delete this college?")) {
			fetch(`/delete_college/${collegeAbbreviation}`, {
				method: "DELETE",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrfToken,
				},
			})
				.then((response) => response.json())
				.then((result) => {
					if (result.success) {
						alert(result.message);
						location.reload();
					} else {
						throw new Error(result.message);
					}
				})
				.catch((error) => {
					alert(error.message);
				});
		}
	});
});
