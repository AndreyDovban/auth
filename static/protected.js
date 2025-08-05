'use strict';

const protected_button = document.querySelector('.protected_button');

protected_button.onclick = () => {
	const token = localStorage.getItem('logint_token');

	if (!token) {
		console.log('token is null');

		return;
	}

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
