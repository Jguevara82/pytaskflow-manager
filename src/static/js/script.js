document.addEventListener('DOMContentLoaded', () => {
	// Obtener referencias a las secciones
	const authSection = document.getElementById('auth-section');
	// Obtener referencias a la sección de tareas
	const tasksSection = document.getElementById('tasks-section');
	// Obtener referencias a los formularios

	const registerForm = document.getElementById('register-form');
	const loginForm = document.getElementById('login-form');
	const logoutButton = document.getElementById('logout-button');

	// Función para ocultar todas las secciones
	function hideAllSections() {
	}

	let authToken = null; // Variable para almacenar el token de autenticación

	// Inicialmente mostrar la sección de autenticación
	authSection.style.display = 'block';
	tasksSection.style.display = 'none';

	// --- Aquí se agregará la lógica para interactuar con el backend ---

	// Function to show a toast message
	function showSwalToast(title, icon = 'info') {
		Swal.fire({
			toast: true,
			position: 'top-end',
			showConfirmButton: false,
			timer: 3000,
			timerProgressBar: true,
			title: title,
			icon: icon
		});
	}

	// Functions for handling authentication
	async function handleRegister(event) {
		event.preventDefault();
		const username = document.getElementById('register-username').value;
		const password = document.getElementById('register-password').value;

		try {
			const response = await fetch('/auth/register', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username,
					password
				})
			});

			const data = await response.json();
			if (response.ok) {
				console.log('Registration successful:', data);
				showSwalToast('Registration successful!', 'success');
			} else {
				console.error('Registration failed:', data.message);
				showSwalToast(`Registration failed: ${data.message}`, 'error');
			}
		} catch (error) {
			console.error('Error during registration:', error)
			showSwalToast('An error occurred during registration.', 'error')
		}
	}

	async function handleLogin(event) {
		event.preventDefault();
		const username = document.getElementById('login-username').value;
		const password = document.getElementById('login-password').value;

		try {
			const response = await fetch('/auth/login', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json'
				},
				body: JSON.stringify({
					username,
					password
				})
			});

			const data = await response.json();
			if (response.ok) {
				console.log('Login successful:', data);
				authToken = data.access_token; // Assuming the backend returns a token in 'access_token'
				localStorage.setItem('authToken', authToken) // Store token in local storage
				showTasksSection(); // Show tasks section after successful login				
				showSwalToast('Login successful!', 'success');
			} else {
				console.error('Login failed:', data.message);
				showSwalToast(`Login failed: ${data.message}`, 'error');
			}
		} catch (error) {
			;
			console.error('Error during login:', error);
			showSwalToast('An error occurred during login.', 'error');
		}
	}

	// Add event listeners for form submissions
	if (registerForm) {
		registerForm.addEventListener('submit', handleRegister);
	}

	if (loginForm) {
		loginForm.addEventListener('submit', handleLogin);
	}

	// Function to show the tasks section after successful login
	function showTasksSection() {
		authSection.style.display = 'none';
		tasksSection.style.display = 'block';
	}

	// Handle logout
	if (logoutButton) {
		logoutButton.addEventListener('click', () => {
			localStorage.removeItem('authToken'); // Remove token from local storage
			authToken = null; // Clear token variable
			authSection.style.display = 'block'; // Show auth section
			tasksSection.style.display = 'none'; // Hide tasks section
			showSwalToast('Logged out successfully!', 'success'); // Show logout success toast
		});
	}
});