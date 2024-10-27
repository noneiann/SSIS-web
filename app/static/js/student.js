document
	.getElementById("submitAddStudent")
	.addEventListener("click", function () {
		const name = document.getElementById("studentName").value;
		const yearLevel = document.getElementById("yearLevel").value;
		const enrollmentStatus = document.getElementById("enrollmentStatus").value;
		const program = document.getElementById("program").value;
		const errorDiv = document.querySelector(".error");
		const csrfToken = document.querySelector(
			'#addStudentForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");
		errorDiv.innerText = "";

		if (!name || !yearLevel || !enrollmentStatus || !program) {
			errorDiv.innerText = "Please fill out all fields.";
			errorDiv.classList.remove("d-none");
			return;
		}

		// Perform AJAX request to add the student (Assuming you have the URL set up)
		fetch("/add_student", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				name: name,
				yearLevel: yearLevel,
				enrollmentStatus: enrollmentStatus,
				program: program,
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

function populateEditModal(studentId, name, yearLevel, enrollmentStatus) {
	document.getElementById("editStudentId").value = studentId;
	document.getElementById("editStudentName").value = name;
	document.getElementById("editYearLevel").value = yearLevel;
	document.getElementById("editEnrollmentStatus").value = enrollmentStatus;
}
document.querySelectorAll(".btn-edit").forEach((button) => {
	button.addEventListener("click", function () {
		const row = this.closest("tr");
		const studentId = this.dataset.id;
		const name = row.cells[1].textContent;
		const yearLevel = row.cells[2].textContent;
		const enrollmentStatus = row.cells[3].textContent;

		populateEditModal(studentId, name, yearLevel, enrollmentStatus);
		new bootstrap.Modal(document.getElementById("editStudentModal")).show();
	});
});

document
	.getElementById("submitEditStudent")
	.addEventListener("click", function () {
		const studentId = document.getElementById("editStudentId").value;
		const name = document.getElementById("editStudentName").value;
		const yearLevel = document.getElementById("editYearLevel").value;
		const enrollmentStatus = document.getElementById(
			"editEnrollmentStatus"
		).value;
		const errorDiv = document.querySelector("#editStudentModal .error");
		const csrfToken = document.querySelector(
			'#editStudentForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");

		if (!name || !yearLevel || !enrollmentStatus) {
			errorDiv.innerText = "Please fill out all fields.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch(`/update_student/${studentId}`, {
			method: "PUT",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				name: name,
				yearLevel: yearLevel,
				enrollmentStatus: enrollmentStatus,
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
		const studentId = this.dataset.id;
		const csrfToken = document.querySelector(
			'#addStudentForm input[name="csrf_token"]'
		).value;

		if (confirm("Are you sure you want to delete this student?")) {
			fetch(`/delete_student/${studentId}`, {
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
