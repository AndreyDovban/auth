'use strict';

const form = document.querySelector('.form');
const list = document.querySelector('.list');

form.addEventListener('submit', e => {
	e.preventDefault();

	const formData = new FormData(form);

	console.log(formData.get('name'));

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

			list.innerHTML = null;

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
				list.append(tr);
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
