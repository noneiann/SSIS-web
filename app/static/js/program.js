document
	.getElementById("submitAddProgram")
	.addEventListener("click", function () {
		const programCode = document.getElementById("courseCode").value;
		const programName = document.getElementById("name").value;
		const college = document.getElementById("college").value;
		const errorDiv = document.querySelector(".error");
		const csrfToken = document.querySelector(
			'#addProgramForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");
		errorDiv.innerText = "";

		if (programCode === "") {
			errorDiv.innerText = "Program Code is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		if (programName === "") {
			errorDiv.innerText = "Program Name is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch("/add_program", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				courseCode: programCode,
				name: programName,
				college: college,
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
		const programId = this.dataset.id;
		const courseCode = row.cells[1].textContent;
		const name = row.cells[2].textContent;
		const college = row.cells[3].textContent;
		// Populate edit modal
		document.getElementById("editProgramId").value = programId;
		document.getElementById("editCourseCode").value = courseCode;
		document.getElementById("editProgramName").value = name;
		document.getElementById("editCollege").value = college;

		new bootstrap.Modal(document.getElementById("editProgramModal")).show();
	});
});

document
	.getElementById("submitEditProgram")
	.addEventListener("click", function () {
		const programId = document.getElementById("editProgramId").value;
		const courseCode = document.getElementById("editCourseCode").value;
		const name = document.getElementById("editProgramName").value;
		const college = document.getElementById("editCollege").value;
		const errorDiv = document.querySelector("#editProgramModal .error");
		const csrfToken = document.querySelector(
			'#editProgramForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");

		if (!courseCode || !name) {
			errorDiv.innerText = "Please fill out all required fields.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch(`/update_program/${programId}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				courseCode: courseCode,
				name: name,
				college: college,
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
		const programId = this.dataset.id;
		const csrfToken = document.querySelector(
			'#addProgramForm input[name="csrf_token"]'
		).value;

		if (confirm("Are you sure you want to delete this program?")) {
			fetch(`/delete_program/${programId}`, {
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
