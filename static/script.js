'use strict';

const form_add_user = document.querySelector('.form_add_user');
const list_users = document.querySelector('.list_users');

form_add_user.addEventListener('submit', e => {
	e.preventDefault();

	const formData = new FormData(form_add_user);

	console.log(formData.get('name'), formData.get('description'), formData.get('role'), formData.get('password'));

	fetch('/api/user', {
		method: 'POST',
		body: formData,
	})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			getUsers();
		})
		.catch(error => {
			console.error('Ошибка отправки:', error);
		});
});

window.onload = getUsers;

function getUsers() {
	fetch('/api/user')
		.then(response => response.json())
		.then(data => {
			console.log(data);

			list_users.innerHTML = null;

			for (const row of data) {
				const tr = document.createElement('tr');
				for (const el of row) {
					const td = document.createElement('td');
					td.innerText = el;
					tr.append(td);
				}
				const td = document.createElement('td');
				const del = document.createElement('button');
				del.innerText = 'del';
				td.append(del);
				del.onclick = () => deleteUser(row[0]);
				tr.append(td);
				list_users.append(tr);
			}
		})
		.catch(error => {
			console.error('Ошибка отправки:', error);
		});
}

function deleteUser(id) {
	fetch('/api/user', {
		method: 'DELETE',
		headers: {
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ id: id }),
	})
		.then(response => response.json())
		.then(data => {
			console.log(data);
			getUsers();
		})
		.catch(error => {
			console.error('Ошибка отправки:', error);
		});
}
