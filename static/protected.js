'use strict';

const protected_button = document.querySelector('.protected_button');

protected_button.onclick = () => {
	console.log('fetch protected');

	const token = localStorage.getItem('logint_token');

	fetch('/protected', {
		method: 'GET',
		headers: {
			ContentType: 'application/json',
			Authorization: `Bearer ${token}`,
		},
	})
		.then(res => res.json())
		.then(res => {
			console.log(res);
		})
		.catch(err => {
			console.log(err.message);
		});
};
