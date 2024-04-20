import React from "react";
import { useState } from "react";

function ContactForm({ existingContact = {}, updateCallback }) {
	const [firstName, setFirstName] = useState(existingContact.firstName || "");
	const [lastName, setLastName] = useState(existingContact.lastName || "");
	const [email, setEmail] = useState(existingContact.email || "");

	const updating = Object.entries(existingContact).length !== 0;

	const onSubmit = async (ele) => {
		ele.preventDefault(); // prevent automatic refresh

		const data = {
			// will auto create keys with the same name as value
			firstName,
			lastName,
			email,
		};
		const url =
			"http://127.0.0.1:5000/" +
			(updating
				? `update_contact/${existingContact.id}`
				: "create_contact");
		const options = {
			method: updating ? "PATCH" : "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify(data),
		};
		const response = await fetch(url, options);

		if (response.status === 201 || response.status === 200) {
			updateCallback();
		} else {
			const data = await response.json();
			alert(data.message);
		}
	};

	return (
		<form onSubmit={onSubmit}>
			<div>
				<label htmlFor="firstName">First Name: </label>
				<input
					type="text"
					id="firstName"
					value={firstName}
					onChange={(ele) => setFirstName(ele.target.value)}
				/>
			</div>
			<div>
				<label htmlFor="lastName">Last Name: </label>
				<input
					type="text"
					id="lastName"
					value={lastName}
					onChange={(ele) => setLastName(ele.target.value)}
				/>
			</div>
			<div>
				<label htmlFor="email">Email: </label>
				<input
					type="text"
					id="email"
					value={email}
					onChange={(ele) => setEmail(ele.target.value)}
				/>
			</div>
			<button type="submit">{updating ? "Update" : "Create"}</button>
		</form>
	);
}

export default ContactForm;
