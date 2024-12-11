document
	.getElementById("submitAddStudent")
	.addEventListener("click", async function () {
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
		const imageFile = document.getElementById("studentImage").files[0];
		const submitButton = document.getElementById("submitAddStudent");
		console.log(imageFile);

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

		try {
			let imageUrl = null;
			submitButton.disabled = true;
			submitButton.textContent = "Uploading Image...";

			if (imageFile) {
				const formData = new FormData();
				const studentId = `${idYear}-${idNumber}`;
				formData.append("studentId", studentId);
				formData.append("image", imageFile);

				const uploadResponse = await fetch("/upload_image", {
					method: "POST",
					headers: {
						"X-CSRFToken": csrfToken,
					},
					body: formData,
				});

				const uploadResult = await uploadResponse.json();
				if (!uploadResponse.ok) {
					throw new Error(uploadResult.error || "Image upload failed");
				}
				submitButton.disabled = false;
				submitButton.textContent = "Add Student";
				imageUrl = uploadResult.url;
			}

			const response = await fetch("/add_student", {
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
					image: imageUrl,
				}),
			});

			const result = await response.json();
			if (result.success) {
				alert(result.message);
				location.reload();
			} else {
				throw new Error(result.message);
			}
		} catch (error) {
			errorDiv.innerText =
				error.message || "An error occurred. Please try again.";
			errorDiv.classList.remove("d-none");
			console.error("Error:", error);
		}
	});

document.querySelectorAll(".btn-edit").forEach((button) => {
	button.addEventListener("click", function () {
		const row = this.closest("tr");
		const studentId = this.dataset.id;
		const name = row.cells[2].textContent;
		const yearLevel = row.cells[3].textContent;
		const enrollmentStatus = row.cells[4].textContent;
		const programId = row.cells[5].dataset.programId;
		const [year, number] = studentId.split("-");

		document.getElementById("editStudentId").value = studentId;
		document.getElementById("editStudentIdYear").value = year;
		document.getElementById("editStudentIdNumber").value = number;
		document.getElementById("editStudentName").value = name;
		document.getElementById("editYearLevel").value = yearLevel;
		document.getElementById("editEnrollmentStatus").value = enrollmentStatus;
		document.getElementById("editProgram").value = programId;
		document.querySelector("#editStudentModal #editImagePreview").src =
			row.cells[0].querySelector("img").src;
		new bootstrap.Modal(document.getElementById("editStudentModal")).show();
	});
});
document
	.getElementById("submitEditStudent")
	.addEventListener("click", async function () {
		const studentId = document.getElementById("editStudentId").value;
		const studentIdYear = document.getElementById("editStudentIdYear").value;
		const studentIdNumber = document.getElementById(
			"editStudentIdNumber"
		).value;
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
		const imageFile = document.getElementById("editStudentImage").files[0];
		const currentImageUrl = document.querySelector(
			"#editStudentModal #editImagePreview"
		).src;
		const submitButton = document.getElementById("submitEditStudent");

		errorDiv.classList.add("d-none");
		errorDiv.innerText = "";

		if (!name || !yearLevel || !enrollmentStatus || !program) {
			errorDiv.innerText = "Please fill out all fields";
			errorDiv.classList.remove("d-none");
			return;
		}

		try {
			let imageUrl = null;
			submitButton.disabled = true;
			submitButton.textContent = "Uploading Image...";
			// If there's a new image file, upload it
			if (imageFile) {
				const formData = new FormData();
				formData.append("image", imageFile);
				formData.append("student_id", studentId);

				const uploadResponse = await fetch("/upload_image", {
					method: "POST",
					headers: {
						"X-CSRFToken": csrfToken,
					},
					body: formData,
				});

				const uploadResult = await uploadResponse.json();
				if (!uploadResponse.ok) {
					throw new Error(uploadResult.error || "Image upload failed");
				}
				imageUrl = uploadResult.url;
				submitButton.disabled = false;
				submitButton.textContent = "Update Student";
			}

			// Send update request
			const response = await fetch(`/update_student/${studentId}`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
					"X-CSRFToken": csrfToken,
				},
				body: JSON.stringify({
					studentIdYear: studentIdYear,
					studentIdNumber: studentIdNumber,
					name: name,
					yearLevel: yearLevel,
					enrollmentStatus: enrollmentStatus,
					program: program,
					image:
						imageUrl ||
						(currentImageUrl.includes("/static/images/default.jpg")
							? null
							: currentImageUrl),
				}),
			});

			const result = await response.json();
			if (result.success) {
				alert(result.message);
				location.reload();
			} else {
				throw new Error(result.message);
			}
		} catch (error) {
			errorDiv.innerText =
				error.message || "An error occurred. Please try again.";
			errorDiv.classList.remove("d-none");
			console.error("Error:", error);
		}
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
function setupImagePreviewAdd() {
	const imageInput = document.getElementById("studentImage");
	const imagePreview = document.getElementById("imagePreview");
	imageInput.addEventListener("change", function (e) {
		const file = e.target.files[0];
		if (file) {
			const reader = new FileReader();

			reader.onload = function (e) {
				imagePreview.src = e.target.result;
				imagePreview.style.display = "block";
			};

			reader.readAsDataURL(file);
		} else {
			imagePreview.src = defaultImageUrl;
			imagePreview.style.display = "none";
		}
	});
}

function setupImagePreviewEdit() {
	const imageInput = document.getElementById("editStudentImage");
	const imagePreview = document.getElementById("editImagePreview");
	imageInput.addEventListener("change", function (e) {
		const file = e.target.files[0];
		if (file) {
			const reader = new FileReader();

			reader.onload = function (e) {
				imagePreview.src = e.target.result;
				imagePreview.style.display = "block";
			};

			reader.readAsDataURL(file);
		} else {
			imagePreview.src = defaultImageUrl;
			imagePreview.style.display = "none";
		}
	});
}

// Add this to your DOMContentLoaded event listener
document.addEventListener("DOMContentLoaded", function () {
	setupImagePreviewAdd();
	setupImagePreviewEdit();
});
