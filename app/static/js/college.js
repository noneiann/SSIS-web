document
	.getElementById("submitAddCollege")
	.addEventListener("click", function () {
		const collegeName = document.getElementById("name").value;
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
		const collegeId = this.dataset.id;
		const name = row.cells[1].textContent;

		// Populate edit modal
		document.getElementById("editCollegeId").value = collegeId;
		document.getElementById("editCollegeName").value = name;

		new bootstrap.Modal(document.getElementById("editCollegeModal")).show();
	});
});

document
	.getElementById("submitEditCollege")
	.addEventListener("click", function () {
		const collegeId = document.getElementById("editCollegeId").value;
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

		fetch(`/update_college/${collegeId}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
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
		const collegeId = this.dataset.id;
		const csrfToken = document.querySelector(
			'#addCollegeForm input[name="csrf_token"]'
		).value;

		if (confirm("Are you sure you want to delete this college?")) {
			fetch(`/delete_college/${collegeId}`, {
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
