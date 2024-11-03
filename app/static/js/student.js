document
	.getElementById("submitAddStudent")
	.addEventListener("click", function () {
		const idYear = document.getElementById("studentIdYear").value;
		const idNumber = document.getElementById("studentIdNumber").value;
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

		// Validate ID format
		if (!idYear || !idNumber) {
			errorDiv.innerText = "Student ID is required.";
			errorDiv.classList.remove("d-none");
			return;
		}

		if (idYear.length !== 4 || idNumber.length !== 4) {
			errorDiv.innerText =
				"ID Year must be 4 digits and ID Number must be 4 digits.";
			errorDiv.classList.remove("d-none");
			return;
		}

		if (!name || !yearLevel || !enrollmentStatus || !program) {
			errorDiv.innerText = "Please fill out all fields.";
			errorDiv.classList.remove("d-none");
			return;
		}

		fetch("/add_student", {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
				"X-CSRFToken": csrfToken,
			},
			body: JSON.stringify({
				studentIdYear: idYear,
				studentIdNumber: idNumber,
				name: name,
				yearLevel: yearLevel,
				enrollmentStatus: enrollmentStatus,
				program: program,
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
				errorDiv.innerText =
					error.message || "An error occurred. Please try again.";
				errorDiv.classList.remove("d-none");
				console.error("Error:", error);
			});
	});

document.querySelectorAll(".btn-edit").forEach((button) => {
	button.addEventListener("click", function () {
		const row = this.closest("tr");
		const studentId = this.dataset.id;
		const name = row.cells[1].textContent;
		const yearLevel = row.cells[2].textContent;
		const enrollmentStatus = row.cells[3].textContent;
		const program = row.cells[4].textContent;

		const [year, number] = studentId.split("-");

		document.getElementById("editStudentId").value = studentId;
		document.getElementById("editStudentIdYear").value = year;
		document.getElementById("editStudentIdNumber").value = number;
		document.getElementById("editStudentName").value = name;
		document.getElementById("editYearLevel").value = yearLevel;
		document.getElementById("editEnrollmentStatus").value = enrollmentStatus;
		document.getElementById("editProgram").value = program;

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
		const program = document.getElementById("editProgram").value;
		const errorDiv = document.querySelector("#editStudentModal .error");
		const csrfToken = document.querySelector(
			'#editStudentForm input[name="csrf_token"]'
		).value;

		errorDiv.classList.add("d-none");

		if (!name || !yearLevel || !enrollmentStatus || !program) {
			errorDiv.innerText = "Please fill out all fields";
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
				program: program,
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

document.querySelectorAll(".idField").forEach((field) => {
	field.addEventListener("input", function () {
		this.value = this.value.replace(/\D/g, "");
	});
});
