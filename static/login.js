'use strict';

const form_auth = document.querySelector('.form_auth');

form_auth.addEventListener('submit', e => {
	e.preventDefault();

	const formData = new FormData(form_auth);

	console.log(formData.get('name'), formData.get('password'));

	fetch('/api/login', {
		method: 'POST',
		body: formData,
	})
		.then(response => response.json())
		.then(data => {
			console.log(data);
		})
		.catch(error => {
			console.error('Ошибка отправки:', error);
		});
});
